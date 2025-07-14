1.该项目敬献给深圳大学南特金融科技学院年轻的社团————AI Club
2.项目分为三个部分，Brain，Front（end），Model from blender。
3.Brain负责整个模型的输入运算和输出逻辑，其中目录下的api文件夹中的api.py文件存放着使用模型的API密钥，IP等信息，
为后期更换模型提供模块化支持。memory文件夹中的json文件存放着可被调用的所有规范记忆，py文件则是按照用户提示词查找
记忆的逻辑函数。logic尚未用到，可以承载后期或许会需要的情绪判断，快捷查询（如时间，天气等）的函数。main文件是主文
件，作为项目的核心主体。
4.Model from blender中存放着数字的形象，目前为ready player me粗略生成的，有待打磨。
5.Front中是vue框架，是项目呈现给用户的前端，直接讲/Project/Front/src/App.vue打开即可
6.先打开Server，再运行.vue
7.本地运行端口号为5200.

##### 当下的任务是
    1优化互动
    2找合适的AI模型（建议借用学校的服务器本地部署deepseek）-> 改变api文件夹里的api.py文件即可
    3优化memory.json文件，收集信息
    4数字人外观打磨，贴合学院
    5.UI再设计再讨论
    6.人物动画可以从Mixamo搬
    7.实现跨域访问服务器

### 关键技术（还没研究完T.T）：
    three.js
    track
    跨域交互



# 🌟 本地运行方法（Mac & Windows 通用）
## 请确保你已安装好 Python 3.9+ 和 Node.js（建议 v18+），否则建议先配置环境
### 第一步：后端启动（Flask）

cd Project                             # 进入到Project路径下，准确来说应该是cd ../../.../Project
python3 -m venv .venv                  # 第一次运行创建虚拟环境
source .venv/bin/activate              ## Windows 用 .venv\Scripts\activate ##
pip install -r requirements.txt        # 安装依赖
cd Brain
python3 Server.py                      # 启动后端服务器

### 第二步： 前端启动（Vue）
cd Project/Front/digital-human-front
npm install                            # 只需第一次执行
npm run dev                            # 启动 Vue 前端（默认端口 5200）

### 第三步： 打开网页
理论上时这个本地网址：http://localhost:5200 