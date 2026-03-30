from openai import OpenAI
import os




class OpenAICompattibleClient:
    """
    调用OpenAi接口的LLM服务的客户端
    """
    def __int__(self,model:str = None,api_key:str = None,base_url:str = None,timeout:int = None):
        # 获得LLM的配置文件
        self.model = model or os.getenv("LLM_MODEL_ID")
        api_key = api_key or os.getenv("LLM_API_KEY")
        base_url = base_url or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT,60"))
        
        if not all([self.model,api_key,base_url]):
            raise ValueError("配置文件加载失败：请检查配置文件")
        
        self.cilent = OpenAI(api_key=api_key,base_url=base_url)
        ## 用户的提示词
    def generate(self,prompt:str,system_prompt:str) -> str:
        """
        调用LLM API来生成回应
        """
        print(f"正在调用{self.model}模型")
        try:
            #打包信息，并且先让AI对系统提示词进行阅读
            
            messages = [
                {'role':'system','content':system_prompt},
                {'role':'user','content':prompt}
            ]
            #返回获取的结果
            response = self.cilent.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.conntent
            print("大语言模型相应成功")
            return answer
        except Exception as e:
            print(f"调用LLM API时发生错误:{e}")
            return "错误:调用语言模型服务时出现错误"
            