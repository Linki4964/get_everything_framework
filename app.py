import os

from flask import Flask, render_template, request, session

from agent import handle_agent_message
from storage import ScanResultStore
from subdomain_collection import run_subdomain_collection


app = Flask(__name__, template_folder="web/templates")
# 中文注释：用于保存对话历史，生产环境请使用安全随机密钥
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")


def normalize_domain(value):
    if value is None:
        return None

    normalized = value.strip().lower()
    if not normalized:
        return None

    return normalized


def _to_ui_history(history):
    # 中文注释：过滤 system 消息，避免在页面上展示系统提示词
    if not history:
        return []
    return [item for item in history if item.get("role") in {"user", "assistant"}]


def build_page_context(
    store,
    domain=None,
    scan_message=None,
    scan_error=None,
    scan_report=None,
    chat_error=None,
):
    summary = store.get_global_summary()
    domain_results = store.get_results_by_domain(domain) if domain else []
    domain_summary = store.get_domain_summary(domain) if domain else None

    raw_history = session.get("agent_history", [])
    raw_steps = session.get("agent_steps", [])

    return {
        "current_domain": domain or "",
        "scan_message": scan_message,
        "scan_error": scan_error,
        "scan_report": scan_report,
        "chat_error": chat_error,
        "summary": summary,
        "domain_summary": domain_summary,
        "domain_results": domain_results,
        "agent_history": _to_ui_history(raw_history),
        "agent_steps": raw_steps,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    store = ScanResultStore()
    domain = normalize_domain(request.values.get("domain"))
    scan_message = None
    scan_error = None
    scan_report = None
    chat_error = None

    if request.method == "POST":
        action = request.form.get("action", "scan")

        if action == "scan":
            if not domain:
                scan_error = "请输入要扫描的域名。"
            else:
                try:
                    scan_report = run_subdomain_collection(
                        domain=domain,
                        tools=["subfinder"],
                        store=store,
                    )
                    scan_message = f"{domain} 扫描完成。"
                except SystemExit as exc:
                    code = exc.code if isinstance(exc.code, int) else 1
                    scan_error = f"扫描未完成，退出码: {code}"
                except Exception as exc:
                    scan_error = f"扫描失败: {exc}"

        elif action == "chat":
            user_message = request.form.get("agent_message", "").strip()
            if not user_message:
                chat_error = "请输入聊天内容。"
            else:
                history = session.get("agent_history", [])
                try:
                    agent_reply = handle_agent_message(
                        user_message,
                        store=store,
                        history=history,
                    )
                    if agent_reply.get("focus_domain"):
                        domain = agent_reply["focus_domain"]

                    new_history = agent_reply.get("conversation_history", history)
                    # 中文注释：保留 system + 最近若干轮消息，控制 session 体积
                    session["agent_history"] = new_history[-40:]
                    steps = agent_reply.get("steps", [])
                    all_steps = session.get("agent_steps", [])
                    all_steps.extend(steps)
                    # 中文注释：只保留最近 50 条工具调用日志
                    session["agent_steps"] = all_steps[-50:]
                except Exception as exc:
                    chat_error = f"处理失败: {exc}"

        else:
            scan_error = f"未知操作: {action}"

    context = build_page_context(
        store,
        domain=domain,
        scan_message=scan_message,
        scan_error=scan_error,
        scan_report=scan_report,
        chat_error=chat_error,
    )
    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
