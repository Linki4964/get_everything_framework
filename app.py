from flask import Flask, render_template, request

from storage import ScanResultStore
from subdomain_collection import run_subdomain_collection


app = Flask(__name__, template_folder="web/templates")


def normalize_domain(value):
    if value is None:
        return None

    normalized = value.strip().lower()
    if not normalized:
        return None

    return normalized


def build_page_context(store, domain=None, scan_message=None, scan_error=None, scan_report=None):
    summary = store.get_global_summary()
    domain_results = store.get_results_by_domain(domain) if domain else []
    domain_summary = store.get_domain_summary(domain) if domain else None

    return {
        "current_domain": domain or "",
        "scan_message": scan_message,
        "scan_error": scan_error,
        "scan_report": scan_report,
        "summary": summary,
        "domain_summary": domain_summary,
        "domain_results": domain_results,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    store = ScanResultStore()
    domain = normalize_domain(request.values.get("domain"))
    scan_message = None
    scan_error = None
    scan_report = None

    if request.method == "POST":
        if not domain:
            scan_error = "请输入要扫描的域名。"
        else:
            try:
                scan_report = run_subdomain_collection(domain=domain, tools=["subfinder"], store=store)
                scan_message = f"{domain} 扫描完成。"
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 1
                scan_error = f"扫描未完成，退出码: {code}"
            except Exception as exc:
                scan_error = f"扫描失败: {exc}"

    context = build_page_context(
        store,
        domain=domain,
        scan_message=scan_message,
        scan_error=scan_error,
        scan_report=scan_report,
    )
    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
