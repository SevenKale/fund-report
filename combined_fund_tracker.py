# -*- coding: utf-8 -*-
import requests
import json
import time
import random
from datetime import datetime
import concurrent.futures
import threading
import pandas as pd
from bs4 import BeautifulSoup

class FundCategoryClassifier:
    def __init__(self):
        # 定义板块关键词映射 - 更详细和专业
        self.category_keywords = {
            # 国防军工板块
            "军工": ["军工", "国防", "空天", "航天", "航空", "军事", "军民", "军品", "军需", "军转民", "军民融合", "国防科技", "军工科技"],
            
            # 医药生物板块
            "医药": ["医药", "医疗", "生物", "创新药", "健康", "疫苗", "生物医药", "医疗器械", "生物技术", "基因", "细胞", "抗体", "疫苗", "中药", "西药", "生物制品", "医药服务", "CRO", "CDMO"],
            
            # 科技板块
            "科技": ["科技", "TMT", "通信", "电子", "半导体", "芯片", "大数据", "云计算", "物联网", "5G", "6G", "信息技术", "软件", "互联网", "数字化", "智能化", "数字经济"],
            
            # 人工智能板块
            "人工智能": ["人工智能", "AI", "机器学习", "深度学习", "神经网络", "智能算法", "智能系统", "智能技术"],
            
            # 新能源板块
            "新能源": ["新能源", "光伏", "太阳能", "风电", "储能", "电池", "电动车", "氢能", "核能", "生物质能", "地热能", "潮汐能", "清洁能源", "绿色能源", "碳中和", "碳达峰"],
            
            # 新能源汽车板块
            "新能源汽车": ["新能源汽车", "电动车", "电动汽车", "新能源车", "智能汽车", "电动化"],
            
            # 消费板块
            "消费": ["消费", "白酒", "食品", "饮料", "家电", "零售", "消费升级", "新消费", "可选消费", "必选消费", "奢侈品", "化妆品", "服装", "珠宝", "旅游", "酒店", "餐饮", "商超"],
            
            # 金融板块
            "金融": ["银行", "金融", "保险", "证券", "红利", "银行股", "保险股", "券商", "信托", "期货", "基金", "理财", "资管", "投行", "商业银行", "投资银行", "金融科技", "FinTech"],
            
            # 房地产板块
            "地产": ["地产", "房地产", "建筑", "建材", "地产股", "开发商", "物业管理", "商业地产", "住宅地产", "工业地产", "土地开发", "房地产服务", "建筑装饰"],
            
            # 建筑材料板块
            "建筑材料": ["建筑材料", "建材", "水泥", "玻璃", "钢材", "建材股", "建材制造", "建材服务"],
            
            # 农业板块
            "农业": ["农业", "养殖", "种植", "农产品", "农业股", "种植业", "畜牧业", "渔业", "林业", "种子", "化肥", "农药", "农机", "农业服务", "乡村振兴", "智慧农业"],
            
            # 贵金属板块
            "黄金": ["黄金", "贵金属", "有色金属", "黄金股", "白银", "铂金", "钯金", "稀土", "铜", "铝", "锌", "镍", "钴", "锂", "金属矿业", "矿业股"],
            
            # 港股板块
            "港股": ["港股", "恒生", "香港", "港股通", "H股", "红筹股", "蓝筹股", "中概股", "港股科技", "港股消费", "港股金融", "港股地产"],
            
            # 智能制造板块
            "机器人": ["机器人", "智能制造", "工业4.0", "自动化", "工业机器人", "服务机器人", "特种机器人", "智能制造装备", "工业自动化", "数字化制造", "柔性制造", "精益制造"],
            
            # 基建板块
            "基建": ["基建", "基础设施", "工程", "建筑材料", "基建股", "铁路", "公路", "机场", "港口", "水利", "电力", "通信", "城市基础设施", "PPP", "专项债"],
            
            # 传媒板块
            "传媒": ["传媒", "文化", "娱乐", "游戏", "影视", "出版", "广告", "营销", "新媒体", "短视频", "直播", "电竞", "动漫", "IP", "版权", "数字内容"],
            
            # 环保板块
            "环保": ["环保", "节能", "绿色", "环保股", "污水处理", "大气治理", "固废处理", "土壤修复", "环境监测", "环保设备", "环保服务", "碳交易", "ESG", "可持续发展"],
            
            # 教育板块
            "教育": ["教育", "培训", "在线教育", "K12", "职业教育", "高等教育", "学前教育", "教育信息化", "智慧教育", "教育科技", "教育服务", "教育装备"],
            
            # 物流板块
            "物流": ["物流", "快递", "运输", "供应链", "仓储", "配送", "货运", "物流股", "快递股", "运输股", "供应链管理", "智慧物流", "冷链物流", "国际物流"],
            
            # 基金类型分类
            "混合型": ["混合", "混合型", "灵活配置", "平衡配置", "稳健配置", "积极配置"],
            "股票型": ["股票", "股票型", "股票基金", "股票投资", "权益投资"],
            "债券型": ["债券", "债基", "债券基金", "纯债", "一级债基", "二级债基", "可转债", "信用债", "利率债"],
            "货币型": ["货币", "货币基金", "货币市场", "现金管理", "活期理财"],
            "指数型": ["指数", "ETF", "LOF", "指数基金", "被动投资", "量化", "增强指数", "Smart Beta"],
            
            # 新增专业板块
            "汽车": ["汽车", "汽车股", "整车", "零部件", "汽车电子", "智能汽车", "新能源汽车", "传统汽车", "汽车服务", "汽车金融"],
            "化工": ["化工", "化工股", "基础化工", "精细化工", "新材料", "化学制品", "化学原料", "化工新材料", "特种化工"],
            "钢铁": ["钢铁", "钢铁股", "钢铁行业", "钢铁制品", "钢铁贸易", "钢铁物流", "钢铁服务"],
            "煤炭": ["煤炭", "煤炭股", "煤炭开采", "煤炭贸易", "煤炭物流", "煤炭服务", "煤炭化工"],
            "电力": ["电力", "电力股", "发电", "输电", "配电", "电力设备", "电力服务", "清洁电力", "传统电力"],
            "通信": ["通信", "通信股", "通信设备", "通信服务", "5G", "6G", "光通信", "无线通信", "卫星通信"],
            "计算机": ["计算机", "计算机股", "计算机设备", "计算机软件", "计算机服务", "系统集成", "IT服务", "软件开发"],
            "电子": ["电子", "电子股", "电子设备", "电子元件", "电子材料", "电子制造", "电子服务"],
            "半导体": ["半导体", "半导体股", "芯片", "集成电路", "IC", "晶圆", "封装", "测试", "设计", "制造"],
            "光伏": ["光伏", "光伏股", "太阳能", "光伏设备", "光伏材料", "光伏组件", "光伏电站", "光伏服务"],
            "风电": ["风电", "风电股", "风力发电", "风电设备", "风电材料", "风电场", "风电服务"],
            "储能": ["储能", "储能股", "电池", "储能设备", "储能材料", "储能系统", "储能服务", "电化学储能", "物理储能"],
            "消费电子": ["消费电子", "消费电子股", "智能手机", "平板电脑", "笔记本电脑", "智能穿戴", "智能家居", "消费电子设备"],
            "家电": ["家电", "家电股", "白色家电", "黑色家电", "小家电", "智能家电", "家电制造", "家电服务"],
            "食品饮料": ["食品饮料", "食品饮料股", "食品", "饮料", "酒类", "乳制品", "调味品", "休闲食品", "食品加工", "饮料制造"],
            "纺织服装": ["纺织服装", "纺织服装股", "纺织", "服装", "鞋帽", "家纺", "纺织材料", "服装制造", "纺织服务"],
            "轻工制造": ["轻工制造", "轻工制造股", "造纸", "包装", "印刷", "家具", "轻工材料", "轻工设备", "轻工服务"],
            "机械设备": ["机械设备", "机械设备股", "工程机械", "机床", "仪器仪表", "机械制造", "机械服务", "自动化设备"],
            "电气设备": ["电气设备", "电气设备股", "电力设备", "电气控制", "电气自动化", "电气制造", "电气服务"],
            "建筑装饰": ["建筑装饰", "建筑装饰股", "建筑", "装饰", "装修", "建筑设计", "建筑服务", "装饰材料"],
            "公用事业": ["公用事业", "公用事业股", "供水", "供气", "供热", "公共交通", "公共设施", "公共服务"],
            "交通运输": ["交通运输", "交通运输股", "公路", "铁路", "航空", "水运", "城市交通", "交通服务", "物流运输"],
            "商业贸易": ["商业贸易", "商业贸易股", "零售", "批发", "贸易", "商业服务", "商业地产", "商业运营"],
            "休闲服务": ["休闲服务", "休闲服务股", "旅游", "酒店", "餐饮", "娱乐", "休闲服务", "文化服务"],
            "综合": ["综合", "综合股", "多元化", "综合投资", "综合服务", "综合业务"],
            
            # 场内基金板块 - 更专业的分类
            "场内基金": ["场内基金", "ETF", "LOF", "场内交易", "交易所交易", "场内ETF", "场内LOF"],
            "ETF基金": ["ETF", "交易所交易基金", "指数ETF", "行业ETF", "主题ETF", "宽基ETF", "窄基ETF"],
            "ETF联接": ["ETF联接", "联接基金", "FOF", "基金中基金", "基金组合"],
            "LOF基金": ["LOF", "上市型开放式基金", "场内LOF", "场外LOF"]
        }
    
    def classify_fund(self, fund_name):
        """根据基金名称分类"""
        if not fund_name:
            return "未知"
        
        fund_name = fund_name.upper()  # 转换为大写便于匹配
        
        # 按优先级排序的板块（更专业的分类顺序）
        priority_categories = [
            # 核心科技板块
            "科技", "半导体", "计算机", "电子", "通信", "人工智能", "机器人",
            # 新兴产业
            "新能源", "光伏", "风电", "储能", "新能源汽车", "消费电子",
            # 传统优势板块
            "军工", "医药", "消费", "食品饮料", "家电", "汽车",
            # 金融地产
            "金融", "地产", "建筑装饰", "建筑材料",
            # 周期板块
            "化工", "钢铁", "煤炭", "电力", "机械设备", "电气设备",
            # 其他板块
            "农业", "黄金", "港股", "基建", "传媒", "环保", "教育", "物流",
            "纺织服装", "轻工制造", "公用事业", "交通运输", "商业贸易", "休闲服务", "综合",
            # 基金类型分类（按专业程度排序）
            "ETF基金", "LOF基金", "ETF联接", "混合型", "股票型", "债券型", "货币型", "指数型",
            # 其他分类
            "场内基金", "其他"
        ]
        
        # 先检查具体板块
        for category in priority_categories:
            if category in self.category_keywords:
                for keyword in self.category_keywords[category]:
                    if keyword.upper() in fund_name:
                        return category
        
        # 再检查基金类型
        for category in ["混合型", "股票型", "债券型", "货币型", "指数型"]:
            if category in self.category_keywords:
                for keyword in self.category_keywords[category]:
                    if keyword.upper() in fund_name:
                        return category
        
        return "其他"
    
    def get_category_description(self, category):
        """获取板块描述"""
        descriptions = {
            # 核心科技板块
            "科技": "科技板块",
            "半导体": "半导体板块",
            "计算机": "计算机板块",
            "电子": "电子板块",
            "通信": "通信板块",
            "人工智能": "人工智能板块",
            "机器人": "智能制造板块",
            
            # 新兴产业
            "新能源": "新能源板块",
            "光伏": "光伏板块",
            "风电": "风电板块",
            "储能": "储能板块",
            "新能源汽车": "新能源汽车板块",
            "消费电子": "消费电子板块",
            
            # 传统优势板块
            "军工": "国防军工板块",
            "医药": "医药生物板块",
            "消费": "消费板块",
            "食品饮料": "食品饮料板块",
            "家电": "家电板块",
            "汽车": "汽车板块",
            
            # 金融地产
            "金融": "金融板块",
            "地产": "房地产板块",
            "建筑装饰": "建筑装饰板块",
            "建筑材料": "建筑材料板块",
            
            # 周期板块
            "化工": "化工板块",
            "钢铁": "钢铁板块",
            "煤炭": "煤炭板块",
            "电力": "电力板块",
            "机械设备": "机械设备板块",
            "电气设备": "电气设备板块",
            
            # 其他板块
            "农业": "农业板块",
            "黄金": "贵金属板块",
            "港股": "港股板块",
            "基建": "基建板块",
            "传媒": "传媒板块",
            "环保": "环保板块",
            "教育": "教育板块",
            "物流": "物流板块",
            "纺织服装": "纺织服装板块",
            "轻工制造": "轻工制造板块",
            "公用事业": "公用事业板块",
            "交通运输": "交通运输板块",
            "商业贸易": "商业贸易板块",
            "休闲服务": "休闲服务板块",
            "综合": "综合板块",
            
            # 基金类型分类
            "混合型": "混合型基金",
            "股票型": "股票型基金",
            "债券型": "债券型基金",
            "货币型": "货币型基金",
            "指数型": "指数型基金",
            "ETF基金": "交易所交易基金",
            "LOF基金": "上市型开放式基金",
            "ETF联接": "ETF联接基金(FOF)",
            "场内基金": "场内交易基金",
            "其他": "其他类型",
            "未知": "未知类型"
        }
        return descriptions.get(category, "未知类型")

class HoldingsProfitCalculator:
    """持仓收益计算器"""
    def __init__(self):
        """初始化持仓收益计算器"""
        pass
    
    def create_sample_holdings(self):
        """创建示例持仓数据"""
        holdings_data = {
            'chaochao': [
                {'fund_code': '023482', 'fund_name': '万家创新药', 'shares': 800, 'cost_price': 1.1500, 'cost_amount': 920.00},
                {'fund_code': '016573', 'fund_name': '招商银行AH', 'shares': 1200, 'cost_price': 1.0800, 'cost_amount': 1296.00},
                {'fund_code': '004409', 'fund_name': '招商TMT', 'shares': 900, 'cost_price': 1.2500, 'cost_amount': 1125.00},
                {'fund_code': '015740', 'fund_name': '国泰港股通科技', 'shares': 1100, 'cost_price': 1.1800, 'cost_amount': 1298.00},
                {'fund_code': '010364', 'fund_name': '鹏华军工', 'shares': 1000, 'cost_price': 1.2000, 'cost_amount': 1200.00},
                {'fund_code': '013309', 'fund_name': '易方达恒生科技', 'shares': 800, 'cost_price': 1.1000, 'cost_amount': 880.00},
                {'fund_code': '014806', 'fund_name': '国金量化混合', 'shares': 1000, 'cost_price': 1.0500, 'cost_amount': 1050.00},
                {'fund_code': '019571', 'fund_name': '诺安配置混合', 'shares': 900, 'cost_price': 1.0800, 'cost_amount': 972.00},
                {'fund_code': '018388', 'fund_name': '华泰柏瑞港股通红利', 'shares': 1000, 'cost_price': 1.1200, 'cost_amount': 1120.00},
                {'fund_code': '006113', 'fund_name': '汇添富创新药混合A', 'shares': 800, 'cost_price': 1.1500, 'cost_amount': 920.00},
                {'fund_code': '021717', 'fund_name': '招商云计算ETF', 'shares': 1000, 'cost_price': 1.1000, 'cost_amount': 1100.00},
                {'fund_code': '001665', 'fund_name': '平安鑫安混合', 'shares': 900, 'cost_price': 1.0500, 'cost_amount': 945.00},
                {'fund_code': '022435', 'fund_name': '南方中证500', 'shares': 1000, 'cost_price': 1.0800, 'cost_amount': 1080.00},
                {'fund_code': '019919', 'fund_name': '招商中证2000', 'shares': 800, 'cost_price': 1.1000, 'cost_amount': 880.00},
                {'fund_code': '014422', 'fund_name': '弘毅消费混合', 'shares': 1000, 'cost_price': 1.1200, 'cost_amount': 1120.00},
                {'fund_code': '020902', 'fund_name': '招商量化选股', 'shares': 900, 'cost_price': 1.0800, 'cost_amount': 972.00},
                {'fund_code': '021378', 'fund_name': '兴业港股通互联网', 'shares': 800, 'cost_price': 1.1500, 'cost_amount': 920.00},
                {'fund_code': '015401', 'fund_name': '弘毅甄选混合', 'shares': 1000, 'cost_price': 1.1000, 'cost_amount': 1100.00},
            ],
            'yaoyao': [
                {'fund_code': '021172', 'fund_name': '华安北证50A', 'shares': 1500, 'cost_price': 1.0500, 'cost_amount': 1575.00},
                {'fund_code': '015945', 'fund_name': '易方达军工混合', 'shares': 1000, 'cost_price': 1.1200, 'cost_amount': 1120.00},
                {'fund_code': '018647', 'fund_name': '易方达家电龙头', 'shares': 800, 'cost_price': 1.0800, 'cost_amount': 864.00},
                {'fund_code': '015897', 'fund_name': '天弘中证化工', 'shares': 1200, 'cost_price': 1.1500, 'cost_amount': 1380.00},
                {'fund_code': '012349', 'fund_name': '天弘恒生科技', 'shares': 900, 'cost_price': 1.2000, 'cost_amount': 1080.00},
                {'fund_code': '013416', 'fund_name': '永赢医疗器械', 'shares': 1000, 'cost_price': 1.1000, 'cost_amount': 1100.00},
                {'fund_code': '002834', 'fund_name': '华夏锦绣混合', 'shares': 800, 'cost_price': 1.0800, 'cost_amount': 864.00},
                {'fund_code': '003547', 'fund_name': '鹏华丰禄债券', 'shares': 1000, 'cost_price': 1.0500, 'cost_amount': 1050.00},
            ]
        }
        
        # 保存为Excel文件
        with pd.ExcelWriter('holdings_data.xlsx', engine='openpyxl') as writer:
            for user, holdings in holdings_data.items():
                df = pd.DataFrame(holdings)
                df.to_excel(writer, sheet_name=user, index=False)
        
        print("✓ 已创建示例持仓文件: holdings_data.xlsx")
        return holdings_data
    
    def update_holdings_data(self):
        """更新持仓数据文件，确保与当前基金代码列表匹配"""
        print("正在更新持仓数据文件...")
        return self.create_sample_holdings()
    
    def load_holdings_from_excel(self, filename='holdings_data.xlsx'):
        """从Excel文件加载持仓数据"""
        try:
            holdings_data = {}
            excel_file = pd.ExcelFile(filename)
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(filename, sheet_name=sheet_name)
                holdings = []
                
                for _, row in df.iterrows():
                    # 确保基金代码是6位数字格式
                    fund_code = str(row['fund_code']).zfill(6)
                    holding = {
                        'fund_code': fund_code,
                        'fund_name': row['fund_name'],
                        'shares': float(row['shares']),
                        'cost_price': float(row['cost_price']),
                        'cost_amount': float(row['cost_amount'])
                    }
                    holdings.append(holding)
                
                holdings_data[sheet_name] = holdings
            
            print(f"✓ 已加载持仓文件: {filename}")
            return holdings_data
            
        except Exception as e:
            print(f"加载持仓文件失败: {e}")
            print("使用示例持仓数据...")
            return self.create_sample_holdings()
    
    def validate_holdings_data(self, holdings_data, fund_data_dict):
        """验证持仓数据是否与基金数据匹配"""
        if not holdings_data or not fund_data_dict:
            return False
        
        # 获取所有基金代码
        all_fund_codes = set()
        if 'all' in fund_data_dict:
            for fund in fund_data_dict['all']:
                all_fund_codes.add(fund['基金代码'])
        else:
            for fund_list in fund_data_dict.values():
                for fund in fund_list:
                    all_fund_codes.add(fund['基金代码'])
        
        print(f"🔍 验证持仓数据匹配性...")
        print(f"📊 基金数据中的代码数量: {len(all_fund_codes)}")
        print(f"🔍 基金数据中的代码: {sorted(list(all_fund_codes))}")
        
        # 检查持仓数据中的基金代码是否都存在
        missing_codes = []
        for user, holdings in holdings_data.items():
            print(f"💰 检查 {user} 的持仓数据 ({len(holdings)} 只基金)")
            for holding in holdings:
                if holding['fund_code'] not in all_fund_codes:
                    missing_codes.append({
                        'user': user,
                        'fund_code': holding['fund_code'],
                        'fund_name': holding['fund_name']
                    })
                    print(f"⚠️  持仓数据中的基金代码 {holding['fund_code']} ({holding['fund_name']}) 在基金数据中未找到")
        
        if missing_codes:
            print(f"❌ 发现 {len(missing_codes)} 个不匹配的基金代码:")
            for item in missing_codes:
                print(f"  - {item['user']}: {item['fund_code']} ({item['fund_name']})")
            return False
        
        print("✅ 所有持仓数据都匹配成功")
        return True
    
    def calculate_holdings_profit(self, holdings_data, fund_data_dict):
        """根据已获取的基金数据计算持仓收益"""
        results = {}
        
        # 将基金数据转换为字典格式，便于查找
        # 优先使用 'all' 键中的数据，因为它包含了所有基金
        fund_data = {}
        if 'all' in fund_data_dict:
            for fund in fund_data_dict['all']:
                fund_data[fund['基金代码']] = fund
        else:
            # 如果没有 'all' 键，则合并所有用户的数据
            for fund_list in fund_data_dict.values():
                for fund in fund_list:
                    fund_data[fund['基金代码']] = fund
        
        print(f"📊 基金数据: {len(fund_data)} 只")
        
        # 打印所有可用的基金代码，用于调试
        available_codes = list(fund_data.keys())
        print(f"🔍 可用基金代码: {available_codes}")
        
        for user, holdings in holdings_data.items():
            print(f"💰 计算 {user} 持仓收益 ({len(holdings)} 只基金)")
            user_results = {
                'total_cost': 0,
                'total_current_value': 0,
                'total_profit': 0,
                'total_profit_rate': 0,
                'today_profit': 0,
                'today_profit_rate': 0,
                'holdings': []
            }
            
            for holding in holdings:
                fund_code = holding['fund_code']
                fund_info = fund_data.get(fund_code)
                
                if fund_info:
                    # 获取基金数据，处理可能的"N/A"值
                    try:
                        # 对于境外基金，需要特殊处理：最新净值是当前价格，估算净值是上日净值
                        if fund_info.get('板块分类') == '境外基金':
                            current_price = float(fund_info.get('最新净值', 0)) if fund_info.get('最新净值') != 'N/A' else 0
                            yesterday_price = float(fund_info.get('估算净值', 0)) if fund_info.get('估算净值') != 'N/A' else 0
                        else:
                            # 对于其他基金，使用标准逻辑
                            current_price = float(fund_info.get('估算净值', 0)) if fund_info.get('估算净值') != 'N/A' else 0
                            yesterday_price = float(fund_info.get('最新净值', 0)) if fund_info.get('最新净值') != 'N/A' else 0
                    except (ValueError, TypeError):
                        current_price = 0
                        yesterday_price = 0
                    
                    # 持仓信息
                    shares = holding['shares']
                    cost_price = holding['cost_price']
                    cost_amount = holding['cost_amount']
                    
                    # 计算当前价值
                    current_value = shares * current_price
                    yesterday_value = shares * yesterday_price
                    
                    # 计算收益
                    total_profit = current_value - cost_amount
                    total_profit_rate = (total_profit / cost_amount) * 100 if cost_amount > 0 else 0
                    
                    # 计算今日收益
                    today_profit = current_value - yesterday_value
                    today_profit_rate = (today_profit / yesterday_value) * 100 if yesterday_value > 0 else 0
                    
                    # 更新总计
                    user_results['total_cost'] += cost_amount
                    user_results['total_current_value'] += current_value
                    user_results['total_profit'] += total_profit
                    user_results['today_profit'] += today_profit
                    
                    # 保存单个持仓结果
                    holding_result = {
                        'fund_code': fund_code,
                        'fund_name': fund_info.get('基金名称', holding['fund_name']),
                        'shares': shares,
                        'cost_price': cost_price,
                        'cost_amount': cost_amount,
                        'current_price': current_price,
                        'current_value': current_value,
                        'total_profit': total_profit,
                        'total_profit_rate': total_profit_rate,
                        'today_profit': today_profit,
                        'today_profit_rate': today_profit_rate,
                        'change_rate': fund_info.get('估算涨跌率', '0.00'),
                        'category': fund_info.get('板块分类', '未知')
                    }
                    user_results['holdings'].append(holding_result)
                    print(f"✅ 持仓匹配成功: {fund_code} ({fund_info.get('基金名称', holding['fund_name'])})")
                else:
                    print(f"⚠️  未找到基金 {fund_code} ({holding['fund_name']}) 的数据")
                    print(f"💡 该基金可能不在当前获取的基金列表中，或者代码不匹配")
            
            # 计算总收益率
            if user_results['total_cost'] > 0:
                user_results['total_profit_rate'] = (user_results['total_profit'] / user_results['total_cost']) * 100
                user_results['today_profit_rate'] = (user_results['today_profit'] / user_results['total_current_value']) * 100
            
            print(f"📈 {user}: 成本 {user_results['total_cost']:,.0f}, 收益 {user_results['total_profit']:,.0f} ({user_results['total_profit_rate']:+.1f}%)")
            results[user] = user_results
        
        return results
    
    def enhance_fund_data_with_holdings(self, fund_data_dict, profit_results):
        """将持仓收益信息添加到基金数据中"""
        enhanced_dict = {}
        
        for user, fund_list in fund_data_dict.items():
            if user == 'all':
                # 对于'all'键，需要合并所有用户的基金并添加持仓信息
                all_funds = []
                all_holdings = {}
                
                # 合并所有用户的持仓信息
                for user_key in ['chaochao', 'yaoyao']:
                    if user_key in profit_results:
                        user_holdings = profit_results[user_key].get('holdings', [])
                        for holding in user_holdings:
                            fund_code = holding['fund_code']
                            if fund_code not in all_holdings:
                                all_holdings[fund_code] = holding
                
                # 为所有基金添加持仓信息（包括境外基金和ETF基金）
                for user_key in ['chaochao', 'yaoyao']:
                    if user_key in fund_data_dict:
                        for fund in fund_data_dict[user_key]:
                            fund_code = fund['基金代码']
                            enhanced_fund = fund.copy()
                            
                            # 查找对应的持仓信息
                            holding = all_holdings.get(fund_code)
                            if holding:
                                enhanced_fund.update({
                                    '成本单价': f"{holding['cost_price']:.4f}",
                                    '当日收益': f"{holding['today_profit']:,.2f}",
                                    '持仓收益': f"{holding['total_profit']:,.2f}",
                                    '持仓收益率': f"{holding['total_profit_rate']:+.2f}%"
                                })
                            else:
                                # 如果没有持仓信息，填充默认值
                                enhanced_fund.update({
                                    '成本单价': 'N/A',
                                    '当日收益': 'N/A',
                                    '持仓收益': 'N/A',
                                    '持仓收益率': 'N/A'
                                })
                            
                            all_funds.append(enhanced_fund)
                
                # 添加境外基金和ETF基金（这些基金没有持仓信息，但需要显示在'all'中）
                if 'overseas' in fund_data_dict:
                    for fund in fund_data_dict['overseas']:
                        enhanced_fund = fund.copy()
                        enhanced_fund.update({
                            '成本单价': 'N/A',
                            '当日收益': 'N/A',
                            '持仓收益': 'N/A',
                            '持仓收益率': 'N/A'
                        })
                        all_funds.append(enhanced_fund)
                
                if 'etf' in fund_data_dict:
                    for fund in fund_data_dict['etf']:
                        enhanced_fund = fund.copy()
                        enhanced_fund.update({
                            '成本单价': 'N/A',
                            '当日收益': 'N/A',
                            '持仓收益': 'N/A',
                            '持仓收益率': 'N/A'
                        })
                        all_funds.append(enhanced_fund)
                
                enhanced_dict[user] = all_funds
                continue
            
            enhanced_funds = []
            user_profit_data = profit_results.get(user, {})
            user_holdings = user_profit_data.get('holdings', [])
            
            # 创建持仓查找字典
            holdings_lookup = {holding['fund_code']: holding for holding in user_holdings}
            
            for fund in fund_list:
                fund_code = fund['基金代码']
                enhanced_fund = fund.copy()
                
                # 查找对应的持仓信息，只保留4个关键字段
                holding = holdings_lookup.get(fund_code)
                if holding:
                    enhanced_fund.update({
                        '成本单价': f"{holding['cost_price']:.4f}",
                        '当日收益': f"{holding['today_profit']:,.2f}",
                        '持仓收益': f"{holding['total_profit']:,.2f}",
                        '持仓收益率': f"{holding['total_profit_rate']:+.2f}%"
                    })
                else:
                    # 如果没有持仓信息，填充默认值
                    enhanced_fund.update({
                        '成本单价': 'N/A',
                        '当日收益': 'N/A',
                        '持仓收益': 'N/A',
                        '持仓收益率': 'N/A'
                    })
                
                enhanced_funds.append(enhanced_fund)
            
            enhanced_dict[user] = enhanced_funds
        
        return enhanced_dict
    
    def save_profit_report(self, profit_results, filename=None):
        """保存持仓收益报告"""
        if not filename:
            filename = f"持仓收益报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        print(f"调试: 开始生成收益报告，数据包含 {len(profit_results)} 个用户")
        for user, result in profit_results.items():
            print(f"调试: 用户 {user} 有 {len(result.get('holdings', []))} 个持仓")
        
        html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>持仓收益报告</title>
    <style>
body {{
    font-family: 'Microsoft YaHei', Arial, sans-serif;
    margin: 20px;
    background-color: #f5f5f5;
}}
.container {{
    max-width: 1400px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}
h1, h2 {{
    color: #333;
    text-align: center;
}}
.summary-card {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    text-align: center;
}}
.profit-positive {{
    color: #dc3545;
    font-weight: bold;
}}
.profit-negative {{
    color: #28a745;
    font-weight: bold;
}}
.profit-neutral {{
    color: #6c757d;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background-color: white;
}}
th {{
    background-color: #007bff;
    color: white;
    padding: 12px 8px;
    text-align: center;
    font-weight: bold;
}}
td {{
    padding: 10px 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}}
tr:nth-child(even) {{
    background-color: #f8f9fa;
}}
tr:hover {{
    background-color: #e9ecef;
}}
.timestamp {{
    text-align: center;
    color: #6c757d;
    font-size: 14px;
    margin-bottom: 20px;
}}
    </style>
</head>
<body>
    <div class="container">
        <h1>持仓收益报告</h1>
        <div class="timestamp">生成时间: {timestamp}</div>
        
        {summary_sections}
        
        {detail_sections}
    </div>
</body>
</html>"""
        
        # 生成汇总部分
        summary_sections = ""
        detail_sections = ""
        
        for user, result in profit_results.items():
            user_name = "钞钞" if user == "chaochao" else "垚垚"
            
            # 汇总卡片
            summary_sections += f"""
            <div class="summary-card">
                <h2>{user_name}的持仓汇总</h2>
                <p><strong>总投入:</strong> {result['total_cost']:,.2f}</p>
                <p><strong>当前市值:</strong> {result['total_current_value']:,.2f}</p>
                <p><strong>总收益:</strong> <span class="{'profit-positive' if result['total_profit'] > 0 else 'profit-negative' if result['total_profit'] < 0 else 'profit-neutral'}">{result['total_profit']:,.2f} ({result['total_profit_rate']:+.2f}%)</span></p>
                <p><strong>今日收益:</strong> <span class="{'profit-positive' if result['today_profit'] > 0 else 'profit-negative' if result['today_profit'] < 0 else 'profit-neutral'}">{result['today_profit']:,.2f} ({result['today_profit_rate']:+.2f}%)</span></p>
            </div>
            """
            
            # 详细表格
            if result['holdings']:  # 只有当有持仓数据时才显示表格
                detail_sections += f"""
                <h2>{user_name}的持仓明细</h2>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>持仓份额</th>
                            <th>成本价</th>
                            <th>当前价格</th>
                            <th>当前市值</th>
                            <th>总收益</th>
                            <th>总收益率</th>
                            <th>今日收益</th>
                            <th>今日涨跌</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for holding in result['holdings']:
                    detail_sections += f"""
                        <tr>
                            <td>{holding['fund_code']}</td>
                            <td>{holding['fund_name']}</td>
                            <td>{holding['shares']:,.0f}</td>
                            <td>{holding['cost_price']:.4f}</td>
                            <td>{holding['current_price']:.4f}</td>
                            <td>{holding['current_value']:,.2f}</td>
                            <td class="{'profit-positive' if holding['total_profit'] > 0 else 'profit-negative' if holding['total_profit'] < 0 else 'profit-neutral'}">{holding['total_profit']:,.2f}</td>
                            <td class="{'profit-positive' if holding['total_profit_rate'] > 0 else 'profit-negative' if holding['total_profit_rate'] < 0 else 'profit-neutral'}">{holding['total_profit_rate']:+.2f}%</td>
                            <td class="{'profit-positive' if holding['today_profit'] > 0 else 'profit-negative' if holding['today_profit'] < 0 else 'profit-neutral'}">{holding['today_profit']:,.2f}</td>
                            <td class="{'profit-positive' if float(holding['change_rate']) > 0 else 'profit-negative' if float(holding['change_rate']) < 0 else 'profit-neutral'}">{holding['change_rate']}%</td>
                        </tr>
                    """
                
                detail_sections += """
                    </tbody>
                </table>
                """
            else:
                detail_sections += f"""
                <h2>{user_name}的持仓明细</h2>
                <p style="text-align: center; color: #6c757d; padding: 20px;">暂无持仓数据</p>
                """
        
        # 生成HTML文件
        html_content = html_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            summary_sections=summary_sections,
            detail_sections=detail_sections
        )
        
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(html_content)
        
        print(f"✓ 持仓收益报告已保存: {filename}")
        return filename

class OptimizedFundTracker:
    def __init__(self, max_workers=10):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://fund.eastmoney.com/",
            "Origin": "https://fund.eastmoney.com"
        })
        self.classifier = FundCategoryClassifier()
        self.max_workers = max_workers
        self._lock = threading.Lock()
        # 抓取重试参数
        self.retry_attempts = 3
        self.retry_backoff_seconds = 0.4
    
    def _parse_jsonp(self, text):
        """解析 jsonpgz(JSONP) 响应，返回 dict 或 None。"""
        if not text:
            return None
        text = text.strip()
        if not text.startswith("jsonpgz("):
            return None
        # 取括号内内容
        start = text.find("(")
        end = text.rfind(")")
        if start == -1 or end == -1 or end <= start:
            return None
        json_str = text[start + 1:end].strip()
        # 处理空/null
        if not json_str or json_str == "null":
            return None
        try:
            data = json.loads(json_str)
            # 仅当为 dict 且包含基金代码时认为有效
            if isinstance(data, dict) and data.get("fundcode"):
                return data
        except Exception:
            return None
        return None
    
    def _fetch_single_fund(self, fund_code):
        """获取单个基金的实时信息"""
        # 优先 https，其次 http，并附加时间戳参数避免缓存
        ts = str(int(time.time() * 1000))
        url_candidates = [
            f"https://fundgz.1234567.com.cn/js/{fund_code}.js?rt={ts}",
            f"http://fundgz.1234567.com.cn/js/{fund_code}.js?rt={ts}"
        ]
        last_error = None
        for url in url_candidates:
            for attempt in range(self.retry_attempts):
                try:
                    response = self.session.get(url, timeout=8)
                    if response.status_code == 200:
                        data = self._parse_jsonp(response.text)
                        if data:
                            # 检查是否有今日净值
                            jzrq = data.get('jzrq', '')
                            today = datetime.now().strftime('%Y-%m-%d')
                            
                            # 如果净值日期是今天，使用今日净值替换估算净值
                            if jzrq == today:
                                data['gsz'] = data.get('dwjz', data.get('gsz', ''))
                                data['gszzl'] = '0.00'  # 今日净值涨跌率为0
                                data['gztime'] = f"{today} 15:00"  # 更新时间
                            
                            return data
                    else:
                        last_error = f"HTTP {response.status_code}"
                except Exception as e:
                    last_error = str(e)
                # 指数退避 + 抖动
                time.sleep(self.retry_backoff_seconds * (2 ** attempt) + random.uniform(0, 0.2))
        with self._lock:
            if last_error:
                print(f"❌ {fund_code}: {last_error}")
            else:
                print(f"❌ {fund_code}: 未知错误")
        return None
    
    def get_funds_realtime(self, fund_codes):
        """获取基金实时数据 - 并发版本"""
        if isinstance(fund_codes, str):
            fund_codes = [fund_codes]
        
        fund_data = []
        today = datetime.now().strftime('%Y-%m-%d')
        today_funds = 0
        estimate_funds = 0
        
        # 使用线程池并发请求
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_code = {executor.submit(self._fetch_single_fund, code): code for code in fund_codes}
            
            # 收集结果
            for future in concurrent.futures.as_completed(future_to_code):
                code = future_to_code[future]
                try:
                    data = future.result()
                    if data:
                        fund_data.append(data)
                        jzrq = data.get('jzrq', '')
                        if jzrq == today:
                            today_funds += 1
                            with self._lock:
                                print(f"✅ {code} (今日净值)")
                        else:
                            estimate_funds += 1
                            with self._lock:
                                print(f"✅ {code} (估算净值)")
                    else:
                        with self._lock:
                            print(f"❌ {code}")
                except Exception as e:
                    with self._lock:
                        print(f"❌ {code}: {e}")
        
        # 打印净值统计
        print(f"📊 净值: 今日 {today_funds} 只, 估算 {estimate_funds} 只")
        
        return fund_data
    
    def get_fund_history_nav(self, fund_code, days=30):
        """获取基金历史净值数据 - 分页抓取（带冗余缓冲，避免翻页去重后不足）"""
        try:
            print(f"正在获取基金 {fund_code} 的历史净值数据...")
            url = f"http://fund.eastmoney.com/f10/F10DataApi.aspx"
            # 目标天数加入冗余缓冲，避免跨页重复导致数量不足
            buffer_days = max(30, int(days * 0.4))
            target_unique = days + buffer_days
            per_page = 50  # 接口每页尽量取满
            max_pages = 12  # 安全上限，避免过多请求

            unique_by_date = {}
            page = 1
            while len(unique_by_date) < target_unique and page <= max_pages:
                params = {
                    'type': 'lsjz',
                    'code': fund_code,
                    'page': page,
                    'per': per_page,
                    'sdate': '',
                    'edate': ''
                }
                print(f"请求第 {page} 页: {url}?{params}")
                response = self.session.get(url, params=params, timeout=15)
                if response.status_code != 200:
                    print(f"获取基金 {fund_code} 历史数据失败: HTTP {response.status_code} (page={page})")
                    break
                page_rows = self._parse_fund_history_html(response.text)
                if not page_rows:
                    # 没有更多数据
                    print(f"第 {page} 页没有数据")
                    break
                print(f"第 {page} 页获取到 {len(page_rows)} 条数据")
                for row in page_rows:
                    unique_by_date[row['date']] = row
                page += 1
                time.sleep(0.12)

            # 去重后按日期降序，截取所需天数
            deduped = list(unique_by_date.values())
            deduped.sort(key=lambda x: x['date'], reverse=True)
            result = deduped[:days]
            print(f"基金 {fund_code} 最终获取到 {len(result)} 条历史数据")
            return result
        except Exception as e:
            print(f"获取基金 {fund_code} 历史数据失败: {e}")
            return []
    
    def _parse_fund_history_html(self, html_content):
        """解析HTML中的历史净值数据"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', class_='w782 comm lsjz')
            
            if not table:
                # 尝试其他可能的表格选择器
                table = soup.find('table')
                if not table:
                    return []
            
            data = []
            rows = table.find_all('tr')[1:]  # 跳过表头
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    date = cols[0].text.strip()
                    nav = cols[1].text.strip()
                    acc_nav = cols[2].text.strip()
                    change_rate = cols[3].text.strip()
                    
                    try:
                        nav_value = float(nav)
                        data.append({
                            'date': date,
                            'nav': nav_value,
                            'acc_nav': acc_nav,
                            'change_rate': change_rate
                        })
                    except ValueError:
                        continue
            
            # 按日期排序（最新的在前）
            data.sort(key=lambda x: x['date'], reverse=True)
            
            # 返回全部解析到的数据（数量由API参数per控制）
            return data
            
        except Exception as e:
            print(f"解析历史净值HTML失败: {e}")
            return []
    
    def get_fund_history_nav_simple(self, fund_code, days=7):
        """获取基金历史净值的简化版本 - 使用另一个API端点"""
        try:
            # 使用另一个API端点，可能更稳定
            url = f"http://fund.eastmoney.com/f10/F10DataApi.aspx"
            
            params = {
                'type': 'lsjz',
                'code': fund_code,
                'page': 1,
                'per': days
            }
            
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return self._parse_fund_history_html(response.text)
            else:
                print(f"获取基金 {fund_code} 历史数据失败: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"获取基金 {fund_code} 历史数据失败: {e}")
            return []

    def get_overseas_fund_data(self, fund_codes):
        """获取境外基金数据 - 直接使用天天基金网API"""
        overseas_funds = []
        
        for fund_code in fund_codes:
            try:
                # 直接调用天天基金网API获取境外基金数据
                fund_data = self._fetch_overseas_fund(fund_code, fund_code)
                if fund_data:
                    overseas_funds.append(fund_data)
                    print(f"✅ 境外基金: {fund_data.get('name', 'N/A')} ({fund_code})")
                else:
                    print(f"❌ 境外基金数据获取失败: {fund_code}")
                    
            except Exception as e:
                print(f"❌ 境外基金 {fund_code} 处理失败: {e}")
                continue
        
        return overseas_funds
    
    def get_etf_fund_data(self, etf_codes):
        """获取场内ETF基金数据 - 支持 .SZ/.SH 后缀的ETF代码"""
        etf_funds = []
        
        for etf_code in etf_codes:
            try:
                # 调用ETF基金API
                fund_data = self._fetch_etf_fund(etf_code, etf_code)
                if fund_data:
                    etf_funds.append(fund_data)
                    print(f"📊 ETF基金: {fund_data.get('name', 'N/A')} ({etf_code})")
                else:
                    print(f"❌ ETF基金数据获取失败: {etf_code}")
                    
            except Exception as e:
                print(f"❌ ETF基金 {etf_code} 处理失败: {e}")
                continue
        
        return etf_funds
    
    def _map_overseas_fund_code(self, fund_code):
        """境外基金代码映射规则"""
        # 移除后缀，获取纯数字代码
        if '.' in fund_code:
            base_code = fund_code.split('.')[0]
        else:
            base_code = fund_code
        
        # 根据后缀类型返回对应的API代码
        if fund_code.endswith('.OF'):
            # 开放式基金，使用天天基金网API
            return base_code
        elif fund_code.endswith('.SZ'):
            # 深圳交易所，使用深交所API
            return f"SZ{base_code}"
        elif fund_code.endswith('.SH'):
            # 上海交易所，使用上交所API
            return f"SH{base_code}"
        else:
            # 默认使用天天基金网API
            return base_code
    
    def _fetch_overseas_fund(self, fund_code, original_code):
        """获取境外基金数据"""
        try:
            # 优先使用天天基金网实时API
            url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                # 尝试解析JSONP数据
                data = self._parse_jsonp(response.text)
                if data:
                    return self._format_overseas_fund_data(data, original_code)
            
            # 如果实时API失败，尝试获取历史净值数据
            try:
                nav_data = self.get_fund_history_nav_simple(fund_code, 1)
                if nav_data and len(nav_data) > 0:
                    latest = nav_data[0]
                    return self._format_overseas_fund_data_from_nav(latest, original_code)
            except Exception as e:
                print(f"获取历史净值失败: {e}")
            
            return None
            
        except Exception as e:
            print(f"获取境外基金 {original_code} 失败: {e}")
            return None
    
    def _format_overseas_fund_data(self, data, original_code):
        """格式化境外基金数据（JSONP格式）"""
        return {
            'fundcode': original_code,
            'name': data.get('name', '境外基金'),
            'dwjz': data.get('dwjz', 'N/A'),  # 最新净值
            'gsz': data.get('gsz', 'N/A'),    # 估算净值
            'gszzl': data.get('gszzl', 'N/A'), # 估算涨跌率
            'jzrq': data.get('jzrq', 'N/A'),  # 净值日期
            'gztime': data.get('gztime', 'N/A'), # 估值时间
            'is_overseas': True
        }
    
    def _format_overseas_fund_data_from_nav(self, nav_data, original_code):
        """格式化境外基金数据（净值格式）"""
        # 尝试从多个API获取基金名称，如果都失败则使用预定义名称
        fund_name = self._get_overseas_fund_name(original_code)
        
        return {
            'fundcode': original_code,
            'name': fund_name,
            'dwjz': nav_data.get('nav', 'N/A'),
            'gsz': nav_data.get('nav', 'N/A'),
            'gszzl': '0.00',  # 历史净值无法计算涨跌率
            'jzrq': nav_data.get('date', 'N/A'),
            'gztime': 'N/A',
            'is_overseas': True
        }
    
    def _get_overseas_fund_name(self, fund_code):
        """获取境外基金名称的多种方法"""
        # 方法1：预定义的基金名称映射
        predefined_names = {
            "015016": "华安国际龙头(dax)",
            "007280": "摩根日本精选股票",
            "012060": "富国全球消费",
            "000834": "大成纳斯达克",
            "270042": "广发纳斯达克"
        }
        
        if fund_code in predefined_names:
            print(f"✅ 使用预定义名称: {predefined_names[fund_code]}")
            return predefined_names[fund_code]
        
        # 方法2：尝试天天基金网实时API
        try:
            url = f"http://fundgz.1234567.com.cn/js/{fund_code}.js"
            print(f"🔍 尝试天天基金网API: {url}")
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = self._parse_jsonp(response.text)
                if data and data.get('name'):
                    print(f"✅ 天天基金网API成功: {data['name']}")
                    return data['name']
        except Exception as e:
            print(f"⚠️  天天基金网API失败: {e}")
        
        # 方法3：尝试东方财富网基金详情页
        try:
            url = f"http://fund.eastmoney.com/{fund_code}.html"
            print(f"🔍 尝试东方财富网详情页: {url}")
            response = self.session.get(url, timeout=8)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                # 查找基金名称
                name_element = soup.find('div', class_='fundDetail-tit')
                if name_element:
                    name = name_element.get_text().strip()
                    if name:
                        print(f"✅ 东方财富网详情页成功: {name}")
                        return name
        except Exception as e:
            print(f"⚠️  东方财富网详情页失败: {e}")
        
        # 方法4：尝试天天基金网基金详情页
        try:
            url = f"http://fund.10jqka.com.cn/{fund_code}/"
            print(f"🔍 尝试同花顺基金详情页: {url}")
            response = self.session.get(url, timeout=8)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                # 查找基金名称
                title_element = soup.find('title')
                if title_element:
                    title_text = title_element.get_text()
                    if '基金' in title_text:
                        name = title_text.replace('基金', '').replace('_同花顺', '').strip()
                        if name:
                            print(f"✅ 同花顺基金详情页成功: {name}")
                            return name
        except Exception as e:
            print(f"⚠️  同花顺基金详情页失败: {e}")
        
        # 如果所有方法都失败，使用默认名称
        default_name = f"境外基金{fund_code}"
        print(f"⚠️  所有API方法都失败，使用默认名称: {default_name}")
        return default_name
    
    def _fetch_etf_fund(self, etf_code, original_code):
        """获取场内ETF基金数据"""
        try:
            # 解析ETF代码，获取交易所和代码
            if '.' in etf_code:
                base_code = etf_code.split('.')[0]
                exchange = etf_code.split('.')[1]
            else:
                base_code = etf_code
                exchange = 'SZ'  # 默认深交所
            
            # 尝试通过东方财富网ETF接口获取数据
            try:
                if exchange == 'SZ':
                    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=0.{base_code}&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f48,f60,f45"
                elif exchange == 'SH':
                    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=1.{base_code}&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f48,f60,f45"
                else:
                    return None
                
                print(f"正在获取ETF数据: {url}")
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"ETF API响应: {data}")
                    if data and data.get('rc') == 0:
                        payload = data.get('data') or {}
                        if not payload:
                            print("ETF API未返回data节点")
                        # 解析ETF数据（传入data节点）
                        return self._format_etf_fund_data(payload, original_code)
                    else:
                        print(f"ETF API返回错误: {data}")
                        
            except Exception as e:
                print(f"ETF接口调用失败: {e}")
            
            # 如果ETF接口失败，尝试通过基金接口获取
            try:
                # 移除后缀，尝试作为基金代码获取
                clean_code = base_code
                print(f"尝试通过基金接口获取: {clean_code}")
                fund_data = self._fetch_single_fund(clean_code)
                if fund_data:
                    return self._format_etf_fund_data_from_fund(fund_data, original_code)
            except Exception as e:
                print(f"基金接口调用失败: {e}")
            
            # 如果都失败了，返回None
            print(f"所有接口都失败，无法获取ETF数据: {original_code}")
            return None
            
        except Exception as e:
            print(f"获取ETF基金 {original_code} 失败: {e}")
            return None
    
    def _format_etf_fund_data(self, data, original_code):
        """格式化ETF基金数据（东方财富接口）"""
        try:
            # 获取ETF名称
            etf_name = data.get('f58', '')
            if not etf_name:
                # 如果API没有返回名称，使用预定义的名称
                etf_names = {
                    "159513.SZ": "纳斯达克100指数ETF",
                    "513520.SH": "日经ETF",
                    "159919.SZ": "沪深300ETF"
                }
                etf_name = etf_names.get(original_code, f"ETF{original_code}")
            
            # 获取并规范化当前价格（不同接口字段倍率可能不同，做自适应归一）
            raw_price = data.get('f43', 0) or 0
            def normalize_price(v):
                # 根据实际ETF价格范围进行更精确的归一化
                # 纳斯达克100ETF等通常价格在1-2之间，沪深300ETF在3-4之间
                if v <= 0:
                    return 0.0
                
                # 尝试不同的除数，优先选择合理的价格范围
                candidates = [
                    v / 100.0,      # 原始值可能是分
                    v / 1000.0,     # 原始值可能是厘
                    v / 10000.0,    # 原始值可能是毫
                    v / 1.0         # 原始值可能已经是元
                ]
                
                # 优先选择在合理ETF价格范围内的值（0.1 ~ 10）
                for p in candidates:
                    if 0.1 <= p <= 10:
                        return p
                
                # 如果都不在合理范围内，选择最接近1的值
                best_candidate = min(candidates, key=lambda x: abs(x - 1.0))
                return best_candidate
            
            current_price = normalize_price(raw_price)
            
            # 获取昨收盘价（f60字段）
            raw_prev_close = data.get('f60', 0) or 0
            prev_close_price = normalize_price(raw_prev_close)
            
            # 获取涨跌幅
            change_rate = data.get('f170', 0) / 100.0  # 涨跌幅需要除以100
            
            # 获取涨跌额
            change_amount = data.get('f169', 0) / 100.0  # 涨跌额需要除以100
            
            # 获取成交量
            volume = data.get('f47', 0)
            
            # 获取成交额（单位万）
            raw_amount = data.get('f48', 0) or 0
            # 通常为分*股，接口已在万为单位，做自适应
            amount_candidates = [raw_amount / 10000.0, raw_amount / 100000.0]
            amount = amount_candidates[0] if amount_candidates[0] >= 0.01 else amount_candidates[1]
            
            # 获取当前时间，但需要调整为交易时间
            now = datetime.now()
            from datetime import timedelta
            
            # 判断是否为交易日（周一至周五）
            def is_trading_day(date_obj):
                """判断是否为交易日（简单判断：周一至周五）"""
                return date_obj.weekday() < 5  # 0-4 表示周一到周五
            
            # 获取上一个交易日
            def get_prev_trading_day(current_date):
                """获取上一个交易日"""
                prev_day = current_date - timedelta(days=1)
                while not is_trading_day(prev_day):
                    prev_day = prev_day - timedelta(days=1)
                return prev_day
            
            # 判断当前是否为交易时间
            is_trading_time = False
            if is_trading_day(now):
                # 交易时间：9:30-11:30, 13:00-15:00
                if ((9 <= now.hour < 11) or (now.hour == 11 and now.minute <= 30) or 
                    (13 <= now.hour < 15) or (now.hour == 15 and now.minute == 0)):
                    is_trading_time = True
            
            if is_trading_time:
                # 交易时间内，使用当前时间
                trade_time = now
                trade_date = now.strftime('%Y-%m-%d')
            else:
                # 非交易时间，使用上一个交易日的15:00
                prev_trade_day = get_prev_trading_day(now)
                trade_time = prev_trade_day.replace(hour=15, minute=0, second=0, microsecond=0)
                trade_date = prev_trade_day.strftime('%Y-%m-%d')
            
            # 昨收盘价对应的日期（上一个交易日）
            # 无论是否为当天，昨收盘价日期都应该是trade_date的上一个交易日
            trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
            prev_trade_date = get_prev_trading_day(trade_date_obj).strftime('%Y-%m-%d')
            
            return {
                'fundcode': original_code,
                'name': etf_name,
                'dwjz': f"{current_price:.4f}",  # 最新价格（当前价格）
                'gsz': f"{prev_close_price:.4f}",   # 昨收盘价
                'gszzl': f"{change_rate:.2f}",   # 涨跌率
                'jzrq': trade_date,  # 最新净值日期（交易日期）
                'gztime': trade_time.strftime('%Y-%m-%d %H:%M'),  # 估值时间（交易时间）
                'is_etf': True,
                'volume': volume,
                'amount': amount,
                'change_amount': change_amount,
                'prev_trade_date': prev_trade_date  # 昨收盘价对应的日期
            }
        except Exception as e:
            print(f"格式化ETF数据失败: {e}")
            return None
    

    
    def _format_etf_fund_data_from_fund(self, fund_data, original_code):
        """格式化ETF基金数据（基金接口）"""
        try:
            # 将基金数据转换为ETF格式
            etf_data = fund_data.copy()
            etf_data['fundcode'] = original_code
            etf_data['is_etf'] = True
            
            # 添加ETF特有字段
            if 'volume' not in etf_data:
                etf_data['volume'] = 0
            if 'amount' not in etf_data:
                etf_data['amount'] = 0
            if 'change_amount' not in etf_data:
                etf_data['change_amount'] = 0
            
            # 确保名称字段正确
            if 'name' not in etf_data or not etf_data['name']:
                etf_names = {
                    "159513.SZ": "华夏中证机器人ETF",
                    "513520.SH": "华夏中证机器人ETF", 
                    "159919.SZ": "嘉实沪深300ETF"
                }
                etf_data['name'] = etf_names.get(original_code, f"ETF{original_code}")
            
            return etf_data
        except Exception as e:
            print(f"转换ETF数据失败: {e}")
            return None

def get_self_selected_funds(max_workers=10):
    """获取自选基金信息 - 优化版本"""
    tracker = OptimizedFundTracker(max_workers=max_workers)
    
    # 钞钞的基金
    chaochao_fund_codes = [
        "023482",  # 万家创新药
        "016573",  # 招商银行AH
        "015740",  # 国泰港股通科技
        "010364",  # 鹏华军工
        "013309",  # 易方达恒生科技
        "014806",  # 国金量化混合
        "018388",  # 华泰柏瑞港股通红利
        "006113",  # 汇添富创新药混合A
        "001665",  # 平安鑫安混合
        "022435",  # 南方中证500
        "019919",  # 招商中证2000
        "020902",  # 招商量化选股
        "021378",  # 兴业港股通互联网
        "015401",  # 弘毅甄选混合
        "270042",  # 广发纳指100
    ]
    
    # 垚垚的基金
    yaoyao_fund_codes = [
        "021172",  #华安北证50A
        "015945",  #易方达军工混合
        "018647",  #易方达家电龙头
        "015897",  #天弘中证化工
        "012349",  #天弘恒生科技
        "013416",  #永赢医疗器械
        "002834",  #华夏锦绣混合
        "003547",  #鹏华丰禄债券
        "021457",  #易方达红利低波A
        "012725",  #国泰畜牧养殖
        "004253",  #国泰黄金
        "016814",  # 国联中证煤炭
        "015016",  # 华安国际龙头(dax)
        "007280",  # 摩根日本精选股票
        "012060",  # 富国全球消费
        "000834",  # 大成纳斯达克
    ]
    
    # 境外基金（实际可获取的基金代码）
    overseas_fund_codes = [
        "015016",  # 华安国际龙头(dax)
        "007280",  # 摩根日本精选股票
        "012060",  # 富国全球消费
        "000834",  # 大成纳斯达克
        "270042",  # 广发纳指100
    ]
    
    # ETF基金代码（场内交易）
    etf_fund_codes = [
        "159513.SZ",  # 纳斯达克100指数ETF
        "513520.SH",  # 日经ETF
        "159919.SZ",  # 沪深300ETF
    ]
    
    # 合并所有基金代码（包括境外基金）
    my_fund_codes = chaochao_fund_codes + yaoyao_fund_codes + overseas_fund_codes
    
    print("=== 自选基金信息 ===")
    print(f"🔍 并发请求: {max_workers} 线程")
    
    start_time = time.time()
    fund_data_raw = tracker.get_funds_realtime(my_fund_codes)
    end_time = time.time()
    
    print(f"⏱️  耗时: {end_time - start_time:.1f}s, 成功: {len(fund_data_raw)}/{len(my_fund_codes)} 只")
    print("=" * 50)
    
    # 获取境外基金数据
    print("\n=== 境外基金信息 ===")
    overseas_fund_data_raw = tracker.get_overseas_fund_data(overseas_fund_codes)
    print(f"🌍 境外基金: 成功 {len(overseas_fund_data_raw)}/{len(overseas_fund_codes)} 只")
    print("=" * 50)
    
    # 获取ETF基金数据
    print("\n=== ETF基金信息 ===")
    etf_fund_data_raw = tracker.get_etf_fund_data(etf_fund_codes)
    print(f"📊 ETF基金: 成功 {len(etf_fund_data_raw)}/{len(etf_fund_codes)} 只")
    print("=" * 50)
    
    # 按组分类基金数据
    chaochao_fund_data = []
    yaoyao_fund_data = []
    overseas_fund_data = []
    etf_fund_data = []
    
    for fund_info in fund_data_raw:
        if fund_info:
            fund_code = fund_info.get('fundcode', 'N/A')
            fund_name = fund_info.get('name', 'N/A')
            category = tracker.classifier.classify_fund(fund_name)
            category_desc = tracker.classifier.get_category_description(category)
            
            change_rate = fund_info.get('gszzl', 'N/A')
            change_symbol = "+" if change_rate != 'N/A' and float(change_rate) > 0 else ""
            print(f"✅ {fund_name} ({fund_code}) {change_symbol}{change_rate}% [{category}]")
            
            fund_item = {
                "基金代码": fund_code,
                "基金名称": fund_name,
                "板块分类": category,
                "最新净值": fund_info.get("dwjz", "N/A"),
                "估算净值": fund_info.get("gsz", "N/A"),
                "估算涨跌率": fund_info.get("gszzl", "N/A"),
                "净值日期": fund_info.get("jzrq", "N/A"),
                "估值时间": fund_info.get("gztime", "N/A")
            }
            
            # 根据基金代码判断属于哪个组
            if fund_code in chaochao_fund_codes:
                chaochao_fund_data.append(fund_item)
            elif fund_code in yaoyao_fund_codes:
                yaoyao_fund_data.append(fund_item)
            elif fund_code in overseas_fund_codes:
                # 境外基金同时添加到两个用户的基金列表中
                chaochao_fund_data.append(fund_item)
                yaoyao_fund_data.append(fund_item)
    
    # 处理境外基金数据
    for fund_info in overseas_fund_data_raw:
        if fund_info:
            fund_code = fund_info.get('fundcode', 'N/A')
            fund_name = fund_info.get('name', 'N/A')
            
            print(f"🌍 {fund_name} ({fund_code})")
            
            # 获取历史净值数据来计算涨跌幅
            try:
                history = tracker.get_fund_history_nav_simple(fund_code, 2)
                if history and len(history) >= 2:
                    # 最新净值（最近净值）
                    latest_nav = history[0]['nav']
                    # 上日净值
                    prev_nav = history[1]['nav']
                    # 计算涨跌幅
                    if prev_nav > 0:
                        change_rate = ((latest_nav - prev_nav) / prev_nav) * 100
                        change_rate_str = f"{change_rate:.2f}"
                    else:
                        change_rate_str = "0.00"
                    
                    fund_item = {
                        "基金代码": fund_code,
                        "基金名称": fund_name,
                        "板块分类": "境外基金",
                        "最新净值": f"{latest_nav:.4f}",  # 最新净值放在"最新净值"列
                        "估算净值": f"{prev_nav:.4f}",   # 上日净值放在"估算净值"列
                        "估算涨跌率": change_rate_str,
                        "净值日期": history[0]['date'] if len(history) >= 1 else "N/A",  # 最新净值日期
                        "估值时间": history[1]['date'] if len(history) >= 2 else "N/A"   # 上日净值日期
                    }
                else:
                    # 如果没有历史数据，使用原始数据
                    fund_item = {
                        "基金代码": fund_code,
                        "基金名称": fund_name,
                        "板块分类": "境外基金",
                        "最新净值": fund_info.get("dwjz", "N/A"),
                        "估算净值": fund_info.get("gsz", "N/A"),
                        "估算涨跌率": fund_info.get("gszzl", "N/A"),
                        "净值日期": fund_info.get("jzrq", "N/A"),
                        "估值时间": fund_info.get("gztime", "N/A")
                    }
            except Exception as e:
                print(f"处理境外基金 {fund_code} 历史数据时出错: {e}")
                fund_item = {
                    "基金代码": fund_code,
                    "基金名称": fund_name,
                    "板块分类": "境外基金",
                    "最新净值": fund_info.get("dwjz", "N/A"),
                    "估算净值": fund_info.get("gsz", "N/A"),
                    "估算涨跌率": fund_info.get("gszzl", "N/A"),
                    "净值日期": fund_info.get("jzrq", "N/A"),
                    "估值时间": fund_info.get("gztime", "N/A")
                }
            
            overseas_fund_data.append(fund_item)
            # 同时添加到两个用户的基金列表中，确保持仓计算能找到
            chaochao_fund_data.append(fund_item)
            yaoyao_fund_data.append(fund_item)
    
    # 处理ETF基金数据
    for fund_info in etf_fund_data_raw:
        if fund_info:
            fund_code = fund_info.get('fundcode', 'N/A')
            fund_name = fund_info.get('name', 'N/A')
            
            print(f"📊 {fund_name} ({fund_code})")
            
            # ETF基金：最新净值日期应该是最新净值的日期，而不是当日
            # 对于ETF基金，由于是实时交易，最新净值就是当前价格，日期应该是交易日
            fund_item = {
                "基金代码": fund_code,
                "基金名称": fund_name,
                "板块分类": "ETF基金",
                "最新净值": fund_info.get("dwjz", "N/A"),
                "估算净值": fund_info.get("gsz", "N/A"),
                "估算涨跌率": fund_info.get("gszzl", "N/A"),
                "净值日期": fund_info.get("jzrq", "N/A"),  # 最新净值日期
                "估值时间": fund_info.get("gztime", "N/A"),  # 估值时间
                "昨收盘价日期": fund_info.get("prev_trade_date", "N/A")  # 昨收盘价对应的日期
            }
            etf_fund_data.append(fund_item)
            # 同时添加到两个用户的基金列表中，确保持仓计算能找到
            chaochao_fund_data.append(fund_item)
            yaoyao_fund_data.append(fund_item)
    
    # 按照原始定义的顺序排序
    def sort_by_original_order(fund_list, original_order):
        """按照原始定义的顺序排序基金"""
        fund_dict = {fund['基金代码']: fund for fund in fund_list}
        sorted_funds = []
        for code in original_order:
            if code in fund_dict:
                sorted_funds.append(fund_dict[code])
        return sorted_funds
    
    # 按原始顺序排序各组基金
    chaochao_sorted = sort_by_original_order(chaochao_fund_data, chaochao_fund_codes)
    yaoyao_sorted = sort_by_original_order(yaoyao_fund_data, yaoyao_fund_codes)
    overseas_sorted = sort_by_original_order(overseas_fund_data, overseas_fund_codes)
    etf_sorted = sort_by_original_order(etf_fund_data, etf_fund_codes)
    
    # 合并所有基金数据到 'all' 键，确保没有重复
    all_funds = []
    all_codes = set()
    
    # 按优先级添加：自选基金 -> 境外基金 -> ETF基金
    for fund in chaochao_sorted + yaoyao_sorted:
        if fund['基金代码'] not in all_codes:
            all_funds.append(fund)
            all_codes.add(fund['基金代码'])
    
    for fund in overseas_sorted:
        if fund['基金代码'] not in all_codes:
            all_funds.append(fund)
            all_codes.add(fund['基金代码'])
    
    for fund in etf_sorted:
        if fund['基金代码'] not in all_codes:
            all_funds.append(fund)
            all_codes.add(fund['基金代码'])
    
    print(f"📊 合并后的总基金数量: {len(all_funds)} 只")
    print(f"🔍 包含的基金类型: 自选基金({len(chaochao_sorted + yaoyao_sorted)}), 境外基金({len(overseas_sorted)}), 场内基金({len(etf_sorted)})")
    
    return {
        "chaochao": chaochao_sorted,
        "yaoyao": yaoyao_sorted,
        "overseas": overseas_sorted,
        "etf": etf_sorted,
        "all": all_funds
    }

def get_monitor_funds(max_workers=10):
    """获取监控基金信息 - 优化版本"""
    tracker = OptimizedFundTracker(max_workers=max_workers)
    
    monitor_fund_codes = [
        #军工
        "010364",  # 鹏华军工
        "022243",  # 中邮军工混合
        "012842",  # 易方达军工
        "015945",  # 易方达军工混合
        "013566",  # 华夏军工混合
        #黄金
        "021959",  # 南方沪深港黄金
        "020412",  # 永赢沪深港黄金
        "004253",  # 国泰黄金
        #医疗
        "006113",  # 汇添富创新药混合A
        "023482",  # 万家港股创新药
        "017633",  # 汇添富医疗器械
        "024380",  # 平安港股通医疗混合
        "013416",  # 永赢医疗器械
        "014565",  # 天弘沪深港创新药
        "020398",  # 中银医药混合
        "021760",  # 中欧港股创新药
        #银行
        "016573",  # 招商银行AH
        "021457",  # 易方达红利低波A
        "018388",  # 华泰柏瑞港股通红利
        "019026",  # 易方达金融股票
        "006810",  # 泰康香港银行
        #通信
        "022365",  # 永赢智选混合
        "004409",  # 招商TMT
        "022500",  # 国泰全指通信ETF
        "021717",  # 招商云计算ETF
        "019170",  # 天弘沪港深云计算
        "014819",  # 国金新兴价值混合
        "020671",  # 易方达科创板芯片
        "014422",  # 弘毅消费混合
        "018994",  # 中欧数字经济混合
        "023385",  # 平安人工智能
        #机器人
        "020256",  # 中欧机器人
        "020973",  # 易方达机器人
        "015401",  # 弘毅甄选混合
        "018125",  # 永赢制造混合
        #量化
        "014806",  # 国金量化混合
        "020902",  # 招商量化选股
        #新能源
        "017647",  # 易方达光伏
        "015528",  # 弘毅汽车混合
        #传统能源
        "016814",  # 国联中证煤炭
        "015897",  # 天弘中证化工
        "018647",  # 易方达家电龙头
        "011036",  # 嘉实中证稀土
        "012725",  # 国泰畜牧养殖
        "012341",  # 东财食品饮料指数
        #半导体
        "012651",  # 博时半导体
        "019571",  # 诺安配置混合
        "001665",  # 平安鑫安混合
        "014855",  # 嘉实中证半导体
        #指数
        "022435",  # 南方中证500
        "019919",  # 招商中证2000
        "021172",  # 华安北证50A
        "001593",  # 天弘创业板ETF
        #基建
        "004857",  # 广发建筑材料
        #港股通科技
        "015740",  # 国泰港股通科技
        "013309",  # 易方达恒生科技
        "012349",  # 天弘恒生科技
        "024535",  # 平安港股通混合
        "021378",  # 兴业港股通互联网
        "013172",  # 华夏恒生互联网
        #灵活混合
        "002834",  # 华夏锦绣混合
        #债基
        "003547",  # 鹏华丰禄债券
        "018598",  # 兴全招益债券
    ]
    
    print("=== 监控基金信息 ===")
    print(f"🔍 并发请求: {max_workers} 线程")
    
    start_time = time.time()
    fund_data_raw = tracker.get_funds_realtime(monitor_fund_codes)
    end_time = time.time()
    
    print(f"⏱️  耗时: {end_time - start_time:.1f}s, 成功: {len(fund_data_raw)}/{len(monitor_fund_codes)} 只")
    
    # 转换数据格式
    monitor_fund_data = []
    for fund_info in fund_data_raw:
        if fund_info:
            fund_code = fund_info.get('fundcode', 'N/A')
            fund_name = fund_info.get('name', 'N/A')
            category = tracker.classifier.classify_fund(fund_name)
            
            fund_item = {
                "基金代码": fund_code,
                "基金名称": fund_name,
                "板块分类": category,
                "最新净值": fund_info.get("dwjz", "N/A"),
                "估算净值": fund_info.get("gsz", "N/A"),
                "估算涨跌率": fund_info.get("gszzl", "N/A"),
                "净值日期": fund_info.get("jzrq", "N/A"),
                "估值时间": fund_info.get("gztime", "N/A")
            }
            monitor_fund_data.append(fund_item)
    
    # 按照原始定义的顺序排序
    def sort_by_original_order(fund_list, original_order):
        """按照原始定义的顺序排序基金"""
        fund_dict = {fund['基金代码']: fund for fund in fund_list}
        sorted_funds = []
        for code in original_order:
            if code in fund_dict:
                sorted_funds.append(fund_dict[code])
        return sorted_funds
    
    # 按原始顺序排序基金
    sorted_monitor_funds = sort_by_original_order(monitor_fund_data, monitor_fund_codes)
    
    return sorted_monitor_funds





def save_to_excel(fund_data_dict, monitor_funds=None, filename=None):
    """保存数据到Excel文件，包含多个sheet页"""
    if not filename:
        filename = f"我的基金_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    if not fund_data_dict:
        print("\n没有数据可保存")
        return None
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 保存监控基金数据（放在第一位）
            if monitor_funds:
                monitor_df = pd.DataFrame(monitor_funds)
                monitor_df.to_excel(writer, sheet_name='监控基金', index=False)
                print(f"✓ 监控基金数据已保存到sheet页（第一位）")
            
            # 保存钞钞的基金数据（按原始定义顺序）
            if fund_data_dict.get('chaochao'):
                chaochao_df = pd.DataFrame(fund_data_dict['chaochao'])
                chaochao_df.to_excel(writer, sheet_name='钞钞的基金', index=False)
                print(f"✓ 钞钞的基金数据已保存到sheet页（按原始定义顺序）")
            
            # 保存垚垚的基金数据（按原始定义顺序）
            if fund_data_dict.get('yaoyao'):
                yaoyao_df = pd.DataFrame(fund_data_dict['yaoyao'])
                yaoyao_df.to_excel(writer, sheet_name='垚垚的基金', index=False)
                print(f"✓ 垚垚的基金数据已保存到sheet页（按原始定义顺序）")
            
            # 保存境外基金数据（按原始定义顺序）
            if fund_data_dict.get('overseas'):
                overseas_df = pd.DataFrame(fund_data_dict['overseas'])
                overseas_df.to_excel(writer, sheet_name='境外基金', index=False)
                print(f"✓ 境外基金数据已保存到sheet页（按原始定义顺序）")
        
            # 保存合并后的基金数据（包含持仓信息）
            if fund_data_dict.get('all'):
                all_df = pd.DataFrame(fund_data_dict['all'])
                all_df.to_excel(writer, sheet_name='全部基金', index=False)
                print(f"✓ 全部基金数据（含持仓信息）已保存到sheet页")
        
        print(f"💾 Excel: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Excel保存失败: {e}")
        return None

def save_to_html_multi_sheet(fund_data_dict, monitor_funds=None, filename=None):
    """保存数据到HTML文件，支持多sheet页显示"""
    if not filename:
        filename = f"我的基金_{datetime.now().strftime('%Y%m%d')}.html"
    
    if not fund_data_dict:
        print("\n没有数据可保存")
        return None
    
    # HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的基金数据</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }}
        .tab-container {{
            margin-bottom: 20px;
        }}
        .tab-buttons {{
            display: flex;
            border-bottom: 2px solid #007bff;
            margin-bottom: 20px;
        }}
        .tab-button {{
            background-color: #f8f9fa;
            border: none;
            padding: 12px 24px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #495057;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
            transition: all 0.3s;
        }}
        .tab-button:hover {{
            background-color: #e9ecef;
        }}
        .tab-button.active {{
            background-color: #007bff;
            color: white;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background-color: white;
        }}
        th {{
            background-color: #007bff;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
        }}
        td {{
            padding: 10px 8px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e9ecef;
        }}
        .fund-row {{
            cursor: pointer;
        }}
        .fund-row:hover {{
            background-color: #e3f2fd !important;
        }}
        .positive {{
            color: #dc3545;
            font-weight: bold;
        }}
        .negative {{
            color: #28a745;
            font-weight: bold;
        }}
        .neutral {{
            color: #6c757d;
        }}
        .profit-positive {{
            color: #dc3545;
            font-weight: bold;
        }}
        .profit-negative {{
            color: #28a745;
            font-weight: bold;
        }}
        .profit-neutral {{
            color: #6c757d;
        }}
        .category-tag {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            color: white;
            font-weight: bold;
        }}
        /* 分类颜色优化：高对比、可读性强 */
        /* 核心科技板块 - 蓝色系 */
        .category-科技 {{
            background-color: #1565c0;
        }}
        .category-半导体 {{
            background-color: #0d47a1;
        }}
        .category-计算机 {{
            background-color: #1976d2;
        }}
        .category-电子 {{
            background-color: #2196f3;
        }}
        .category-通信 {{
            background-color: #42a5f5;
        }}
        .category-人工智能 {{
            background-color: #1e88e5;
        }}
        .category-机器人 {{
            background-color: #455a64;
        }}
        
        /* 新兴产业 - 绿色系 */
        .category-新能源 {{
            background-color: #2e7d32;
        }}
        .category-光伏 {{
            background-color: #388e3c;
        }}
        .category-风电 {{
            background-color: #4caf50;
        }}
        .category-储能 {{
            background-color: #66bb6a;
        }}
        .category-新能源汽车 {{
            background-color: #81c784;
        }}
        .category-消费电子 {{
            background-color: #a5d6a7;
            color: #2e7d32;
        }}
        
        /* 传统优势板块 - 红色系 */
        .category-军工 {{
            background-color: #c62828;
        }}
        .category-医药 {{
            background-color: #d32f2f;
        }}
        .category-消费 {{
            background-color: #ef6c00;
        }}
        .category-食品饮料 {{
            background-color: #f57c00;
        }}
        .category-家电 {{
            background-color: #ff8f00;
            color: #fff;
        }}
        .category-汽车 {{
            background-color: #e65100;
        }}
        
        /* 金融地产 - 紫色系 */
        .category-金融 {{
            background-color: #6a1b9a;
        }}
        .category-地产 {{
            background-color: #ad1457;
        }}
        .category-建筑装饰 {{
            background-color: #c2185b;
        }}
        .category-建筑材料 {{
            background-color: #d81b60;
        }}
        
        /* 周期板块 - 棕色系 */
        .category-化工 {{
            background-color: #8d6e63;
        }}
        .category-钢铁 {{
            background-color: #6d4c41;
        }}
        .category-煤炭 {{
            background-color: #5d4037;
        }}
        .category-电力 {{
            background-color: #4e342e;
        }}
        .category-机械设备 {{
            background-color: #3e2723;
        }}
        .category-电气设备 {{
            background-color: #bf360c;
        }}
        
        /* 其他板块 - 多样化颜色 */
        .category-农业 {{
            background-color: #00897b;
        }}
        .category-黄金 {{
            background-color: #b58900;
            color: #fff;
        }}
        .category-港股 {{
            background-color: #006064;
        }}
        .category-基建 {{
            background-color: #795548;
            color: #fff;
        }}
        .category-传媒 {{
            background-color: #5d4037;
        }}
        .category-环保 {{
            background-color: #2e7d32;
        }}
        .category-教育 {{
            background-color: #283593;
        }}
        .category-物流 {{
            background-color: #37474f;
        }}
        .category-纺织服装 {{
            background-color: #6a1b9a;
        }}
        .category-轻工制造 {{
            background-color: #8e24aa;
        }}
        .category-公用事业 {{
            background-color: #7b1fa2;
        }}
        .category-交通运输 {{
            background-color: #9c27b0;
        }}
        .category-商业贸易 {{
            background-color: #ba68c8;
            color: #4a148c;
        }}
        .category-休闲服务 {{
            background-color: #ce93d8;
            color: #4a148c;
        }}
        .category-综合 {{
            background-color: #e1bee7;
            color: #4a148c;
        }}
        
        /* 基金类型分类 - 灰色系 */
        .category-混合型 {{
            background-color: #546e7a;
        }}
        .category-股票型 {{
            background-color: #b71c1c;
        }}
        .category-债券型 {{
            background-color: #1b5e20;
        }}
        .category-货币型 {{
            background-color: #795548;
            color: #fff;
        }}
        .category-指数型 {{
            background-color: #00695c;
        }}
        .category-ETF基金 {{
            background-color: #d32f2f;  /* 深红色，更明显 */
            color: #ffffff;
            font-weight: bold;
        }}
        .category-LOF基金 {{
            background-color: #e65100;  /* 橙红色 */
            color: #ffffff;
            font-weight: bold;
        }}
        .category-ETF联接 {{
            background-color: #6a1b9a;  /* 深紫色 */
            color: #ffffff;
            font-weight: bold;
        }}
        
        /* 特殊基金类型 */
        .category-境外基金 {{
            background-color: #4a148c;
        }}
        .category-场内基金 {{
            background-color: #0d47a1;  /* 深蓝色 */
            color: #ffffff;
        }}
        .category-其他 {{
            background-color: #6c757d;
        }}
        .category-未知 {{
            background-color: #6c757d;
        }}
        .timestamp {{
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .section-header {{
            background-color: #e3f2fd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-weight: bold;
            color: #1976d2;
        }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4);
        }}
        .modal-content {{
            background-color: #ffffff;
            color: #333333;
            margin: 2% auto;
            padding: 20px 16px;
            border: 1px solid #ddd;
            width: 92%;
            max-width: 1000px;
            border-radius: 12px;
            position: relative;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            max-height: 92vh;
            overflow-y: auto;
            overflow-x: hidden;
            box-sizing: border-box;
        }}
        .close {{
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            position: absolute;
            right: 20px;
            top: 20px;
            transition: color 0.3s;
        }}
        .close:hover {{
            color: #000000;
        }}
        .chart-container {{
            position: relative;
            height: 500px;
            margin: 16px 0 8px;
            width: 100%;
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            box-sizing: border-box;
        }}
        #navChart {{ width: 100%; }}
        .nav-data {{
            display: none;
        }}
        .cost-line {{
            border-top: 2px dashed #ff6b6b;
            margin: 10px 0;
            padding-top: 10px;
        }}
        .cost-line strong {{
            color: #ff6b6b;
        }}
        .modal-title {{
            color: #333333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 24px;
        }}
        .range-buttons {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 10px;
        }}
        .header-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }}
        .range-section {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .label-strong {{
            font-weight: 700;
        }}
        .range-btn {{
            border: 1px solid #007bff;
            background: #fff;
            color: #007bff;
            padding: 6px 12px;
            border-radius: 16px;
            cursor: pointer;
            font-size: 14px;
        }}
        .range-btn.active {{
            background: #007bff;
            color: #fff;
        }}
        .legend {{
            display: flex;
            align-items: center;
            color: #555;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: inline-flex;
            align-items: center;
            margin-left: 6px;
            font-size: 14px;
        }}
        .legend-line {{
            display: inline-block;
            width: 22px;
            height: 0;
            border-top: 3px solid #007bff;
            margin-right: 6px;
        }}
        .legend-line.price {{
            border-top: 3px solid #007bff;
        }}
        .legend-line.cost {{
            border-top: 2px dashed #ff6b6b;
        }}
        .tooltip {{
            position: fixed; /* 改为固定定位，避免被容器裁剪 */
            background: rgba(0,0,0,0.85);
            color: #fff;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 14px;
            pointer-events: none;
            transform: translate(-50%, -120%);
            white-space: nowrap;
            z-index: 9999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>我的基金数据</h1>
        <div class="timestamp">生成时间: {timestamp}</div>
        
        <!-- 弹框 -->
        <div id="fundModal" class="modal">
            <div class="modal-content">
                <span class="close">&times;</span>
                <h2 class="modal-title" id="modalTitle">基金详情</h2>
                <div class="header-row">
                    <div class="range-section">
                        <span class="label-strong">选择时间</span>
                        <div class="range-buttons">
                            <button class="range-btn active" data-days="30">1月</button>
                            <button class="range-btn" data-days="90">3月</button>
                            <button class="range-btn" data-days="180">6月</button>
                            <button class="range-btn" data-days="365">1年</button>
                        </div>
                    </div>
                    <div class="legend">
                        <span class="legend-item"><span class="legend-line price"></span>净价</span>
                        <span class="legend-item"><span class="legend-line cost"></span>成本单价</span>
                    </div>
                </div>
                <div class="chart-container">
                    <div id="navChart"></div>
                </div>
                <!-- 底部成本价条已移除，改由悬浮展示 -->
            </div>
        </div>
        
        <div class="summary">
            <h3>汇总信息</h3>
            <p>监控基金: <strong>{monitor_count}</strong> 只, 钞钞的基金: <strong>{chaochao_count}</strong> 只, 垚垚的基金: <strong>{yaoyao_count}</strong> 只, 境外基金: <strong>{overseas_count}</strong> 只</p>
            <p>监控基金平均涨跌率: <strong class="{monitor_avg_class}">{avg_change}</strong></p>
            <p>监控基金上涨: <span class="positive">{up_count}</span> 只, 下跌: <span class="negative">{down_count}</span> 只, 平盘: <span class="neutral">{flat_count}</span> 只</p>
            <p>钞钞平均涨跌率: <strong class="{chaochao_avg_class}">{chaochao_avg_change}</strong>，上涨: <span class="positive">{chaochao_up_count}</span> 只, 下跌: <span class="negative">{chaochao_down_count}</span> 只, 平盘: <span class="neutral">{chaochao_flat_count}</span> 只</p>
            <p>垚垚平均涨跌率: <strong class="{yaoyao_avg_class}">{yaoyao_avg_change}</strong>，上涨: <span class="positive">{yaoyao_up_count}</span> 只, 下跌: <span class="negative">{yaoyao_down_count}</span> 只, 平盘: <span class="neutral">{yaoyao_flat_count}</span> 只</p>
            <p>钞钞当日预估收益: <strong class="{chaochao_profit_class}">{chaochao_today_profit}</strong></p>
            <p>垚垚当日预估收益: <strong class="{yaoyao_profit_class}">{yaoyao_today_profit}</strong></p>
        </div>
        
        <div class="tab-container">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="showTab('monitor')">监控基金</button>
                <button class="tab-button" onclick="showTab('chaochao')">钞钞的基金</button>
                <button class="tab-button" onclick="showTab('yaoyao')">垚垚的基金</button>
                <button class="tab-button" onclick="showTab('overseas')">境外基金</button>
                <button class="tab-button" onclick="showTab('etf')">场内基金</button>
            </div>
            
            <div id="monitor" class="tab-content active">
                <h3>监控基金</h3>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>板块分类</th>
                            <th>最新净值<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{latest_date_header}</span></th>
                            <th>估算净值<br><span style="font-size: 12px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{estimate_date_header}</span></th>
                            <th>估算涨跌率</th>
                        </tr>
                    </thead>
                    <tbody>
                        {monitor_table_rows}
                    </tbody>
                </table>
            </div>
            
            <div id="chaochao" class="tab-content">
                <h3>钞钞的基金</h3>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>板块分类</th>
                            <th>最新净值<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{latest_date_header}</span></th>
                            <th>估算净值<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{estimate_date_header}</span></th>
                            <th>估算涨跌率</th>
                            <th>成本单价</th>
                            <th>当日收益</th>
                            <th>持仓收益</th>
                            <th>持仓收益率</th>
                        </tr>
                    </thead>
                    <tbody>
                        {chaochao_table_rows}
                    </tbody>
                </table>
            </div>
            
            <div id="yaoyao" class="tab-content">
                <h3>垚垚的基金</h3>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>板块分类</th>
                            <th>最新净值<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{latest_date_header}</span></th>
                            <th>估算净值<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{estimate_date_header}</span></th>
                            <th>估算涨跌率</th>
                            <th>成本单价</th>
                            <th>当日收益</th>
                            <th>持仓收益</th>
                            <th>持仓收益率</th>
                        </tr>
                    </thead>
                    <tbody>
                        {yaoyao_table_rows}
                    </tbody>
                </table>
            </div>
            
            <div id="overseas" class="tab-content">
                <h3>境外基金</h3>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>板块分类</th>
                            <th>最新净值</th>
                            <th>上日净值</th>
                            <th>涨跌幅</th>
                        </tr>
                    </thead>
                    <tbody>
                        {overseas_table_rows}
                    </tbody>
                </table>
            </div>
            
            <div id="etf" class="tab-content">
                <h3>场内基金</h3>
                <table>
                    <thead>
                        <tr>
                            <th>基金代码</th>
                            <th>基金名称</th>
                            <th>板块分类</th>
                            <th>最新净价<br><span style="font-size: 12px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{etf_latest_time_header}</span></th>
                            <th>上日净价<br><span style="font-size: 14px; color: #ffffff; background-color: #007bff; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px;">{etf_prev_date_header}</span></th>
                            <th>涨跌率</th>
                        </tr>
                    </thead>
                    <tbody>
                        {etf_table_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        // API 基址自动探测与可配置（支持 ?api= 覆盖与 localStorage 持久化）
        (function() {{
            function resolveApiBase() {{
                try {{
                    var params = new URLSearchParams(window.location.search);
                    var apiFromQuery = params.get('api');
                    if (apiFromQuery) {{
                        try {{ localStorage.setItem('API_BASE', apiFromQuery); }} catch (e) {{}}
                        return apiFromQuery;
                    }}
                    try {{
                        var saved = localStorage.getItem('API_BASE');
                        if (saved) return saved;
                    }} catch (e) {{}}

                    // 默认策略：
                    // - 如果在 http(s) 环境且有同源后端，可用相对路径
                    // - 如果是 GitHub Pages（github.io），建议配置公开 API 地址
                    var origin = window.location.origin || '';
                    if (/^https?:\\/\\//i.test(origin)) {{
                        if (/github\\.io$/i.test(window.location.hostname)) {{
                            // 在 GitHub Pages 上，强烈建议通过 ?api= 或 localStorage 配置公开可访问的 HTTPS API 基址
                            // 临时回退为同源相对路径，若无后端会 404
                            return origin; 
                        }}
                        return origin;
                    }}
                }} catch (e) {{}}
                // 本地文件或未知协议下的回退
                return 'http://127.0.0.1:5000';
            }}
            window.API_BASE = (resolveApiBase() || '').replace(/\\/$/, '');
        }})();
        function showTab(tabName) {{
            // 隐藏所有tab内容
            var tabContents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove('active');
            }}
            
            // 移除所有tab按钮的active类
            var tabButtons = document.getElementsByClassName('tab-button');
            for (var i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].classList.remove('active');
            }}
            
            // 显示选中的tab内容
            document.getElementById(tabName).classList.add('active');
            
            // 添加active类到选中的按钮
            event.target.classList.add('active');
        }}

        // 弹框相关变量
        var modal = document.getElementById('fundModal');
        var span = document.getElementsByClassName('close')[0];
        var navChart = null;
        var selectedFundCode = null;
        var selectedCostPrice = null;
        var selectedDays = 30;
        var rangeButtons = null;

        // 关闭弹框
        span.onclick = function() {{
            modal.style.display = "none";
            if (navChart) {{
                navChart.destroy();
                navChart = null;
            }}
        }}

        // 点击弹框外部关闭
        window.onclick = function(event) {{
            if (event.target == modal) {{
                modal.style.display = "none";
                if (navChart) {{
                    navChart.destroy();
                    navChart = null;
                }}
            }}
        }}

        // 双击基金行显示弹框
        function showFundDetail(fundCode, fundName, costPrice) {{
            console.log('显示基金详情:', fundCode, fundName, costPrice);
            document.getElementById('modalTitle').textContent = fundName + ' (' + fundCode + ')';
            // 底部成本价区域已移除，改由悬浮提示

            // 显示弹框
            modal.style.display = "block";

            // 记录选择
            selectedFundCode = fundCode;
            selectedCostPrice = costPrice;
            selectedDays = 30;

            // 绑定区间按钮
            rangeButtons = document.getElementsByClassName('range-btn');
            for (var i = 0; i < rangeButtons.length; i++) {{
                rangeButtons[i].classList.remove('active');
                if (rangeButtons[i].getAttribute('data-days') === '30') {{
                    rangeButtons[i].classList.add('active');
                }}
                (function(btn) {{
                    btn.onclick = function() {{
                        for (var j = 0; j < rangeButtons.length; j++) {{
                            rangeButtons[j].classList.remove('active');
                        }}
                        btn.classList.add('active');
                        var days = parseInt(btn.getAttribute('data-days')) || 30;
                        selectedDays = days;
                        loadFundData(selectedFundCode, selectedCostPrice, selectedDays);
                    }}
                }})(rangeButtons[i]);
            }}

            // 加载净值数据和图表（默认1月）
            loadFundData(fundCode, costPrice, selectedDays);
        }}

        // 加载基金数据
        function loadFundData(fundCode, costPrice, days) {{
            console.log('加载基金数据:', fundCode, costPrice);
            days = days || 30;
            
            // 显示加载状态
            var chartContainer = document.getElementById('navChart');
            if (chartContainer) {{
                chartContainer.innerHTML = '<div style="text-align: center; padding: 50px; color: #666;">正在加载历史净值数据...</div>';
            }}
            
            // 调用真实的历史净值API（近30天）- 使用可配置 API_BASE，支持 GitHub Pages 调用公网 HTTPS API
            fetch(window.API_BASE + '/api/fund/history/' + fundCode + '?days=' + days)
                .then(response => {{
                    if (!response.ok) {{
                        throw new Error(`HTTP ${{response.status}}`);
                    }}
                    return response.json();
                }})
                .then(data => {{
                    if (data.success && data.data && data.data.length > 0) {{
                        console.log('获取到真实历史数据:', data);
                        // 转换数据格式以适配图表显示
                        var chartData = data.data.map(function(item) {{
                            return {{
                                date: item.date,
                                nav: item.nav
                            }};
                        }});
                        // 日期升序排列，保证从左到右递增
                        chartData.sort(function(a, b) {{
                            return new Date(a.date) - new Date(b.date);
                        }});
                        var label = '近' + (days === 30 ? '1月' : days === 90 ? '3月' : days === 180 ? '6月' : '1年') + '净值走势';
                        displayChart(chartData, fundCode, costPrice, label);
                    }} else {{
                        console.error('API返回数据为空:', data);
                        if (chartContainer) {{
                            chartContainer.innerHTML = '<div style="text-align: center; padding: 50px; color: #c00;">未获取到历史净值数据（API无数据）</div>';
                        }}
                    }}
                }})
                .catch(error => {{
                    console.error('获取历史净值数据失败:', error);
                    if (chartContainer) {{
                        chartContainer.innerHTML = '<div style="text-align: center; padding: 50px; color: #c00;">获取历史净值数据失败。<br/>'
                          + '当前 API_BASE: ' + (window.API_BASE || '(未设置)') + '<br/>'
                          + '如在 GitHub Pages，请在 URL 追加 ?api=https://你的API域名 或在本地打开后设置 localStorage.API_BASE</div>';
                    }}
                }});
        }}

        /* 模拟数据逻辑已禁用以便排查真实API问题
        function generateMockData(fundCode) {{}}
        */

        // 显示图表
        function displayChart(data, fundCode, costPrice, titleLabel) {{
            console.log('开始绘制SVG图表:', data, fundCode, costPrice, titleLabel);
            
            var chartContainer = document.getElementById('navChart');
            if (!chartContainer) {{
                console.error('找不到图表容器元素');
                return;
            }}
            
            // 清空容器
            chartContainer.innerHTML = '';
            // 创建 tooltip 容器
            var tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.style.display = 'none';
            document.body.appendChild(tooltip);
            
            // X轴标签稀疏显示：优先显示每月1日；若无，则显示每月15日；否则按间隔抽样
            var labels = [];
            var labelIndices = [];
            for (var i = 0; i < data.length; i++) {{
                var d = new Date(data[i].date);
                var day = d.getDate();
                if (day === 1 || day === 15) {{
                    labels.push((d.getMonth()+1) + '/' + day);
                    labelIndices.push(i);
                }}
            }}
            if (labels.length < 4) {{
                // 兜底：按固定间隔取4个点
                labels = [];
                labelIndices = [];
                var steps = 3;
                for (var s = 0; s <= steps; s++) {{
                    var idx = Math.round(s * (data.length - 1) / steps);
                    var dd = new Date(data[idx].date);
                    labels.push((dd.getMonth()+1) + '/' + dd.getDate());
                    labelIndices.push(idx);
                }}
            }}
            var values = data.map(function(item) {{
                return parseFloat(item.nav);
            }});
            
            console.log('图表标签:', labels);
            console.log('图表数值:', values);

            // 计算SVG尺寸
            var width = chartContainer.clientWidth - 24;
            var height = 400;
            var paddingLeft = 54, paddingRight = 16, paddingTop = 32, paddingBottom = 46;
            var chartWidth = width - paddingLeft - paddingRight;
            var chartHeight = height - paddingTop - paddingBottom;
            
            // 计算数据范围
            var minValue = Math.min(...values);
            var maxValue = Math.max(...values);
            var valueRange = maxValue - minValue;
            if (valueRange === 0) valueRange = 0.1;
            
            // 如果有成本价，调整范围
            if (costPrice && costPrice !== 'N/A') {{
                try {{
                    var costValue = parseFloat(costPrice);
                    if (!isNaN(costValue)) {{
                        minValue = Math.min(minValue, costValue);
                        maxValue = Math.max(maxValue, costValue);
                        valueRange = maxValue - minValue;
                        if (valueRange === 0) valueRange = 0.1;
                    }}
                }} catch (e) {{
                    console.log('成本价解析失败:', e);
                }}
            }}
            
            // 创建SVG元素
            var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svg.setAttribute('width', width);
            svg.setAttribute('height', height);
            svg.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
            
            // 添加网格线（减少密度）
            for (var i = 0; i <= 4; i++) {{
                var y = paddingTop + (i * chartHeight / 4);
                var gridLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                gridLine.setAttribute('x1', paddingLeft);
                gridLine.setAttribute('y1', y);
                gridLine.setAttribute('x2', width - paddingRight);
                gridLine.setAttribute('y2', y);
                gridLine.setAttribute('stroke', '#e0e0e0');
                gridLine.setAttribute('stroke-width', '1');
                svg.appendChild(gridLine);
            }}
            
            // 添加Y轴标签（5-6档稀疏显示）
            var yTicksCount = 5;
            for (var i = 0; i <= yTicksCount; i++) {{
                var y = paddingTop + (i * chartHeight / yTicksCount);
                var value = maxValue - (i * valueRange / yTicksCount);
                var text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', paddingLeft - 10);
                text.setAttribute('y', y + 4);
                text.setAttribute('text-anchor', 'end');
                text.setAttribute('font-size', '12');
                text.setAttribute('fill', '#666');
                text.textContent = value.toFixed(3);
                svg.appendChild(text);
            }}
            
            // 绘制净值曲线
            var points = [];
            for (var i = 0; i < values.length; i++) {{
                var x = paddingLeft + (i * chartWidth / (values.length - 1));
                var y = paddingTop + ((maxValue - values[i]) * chartHeight / valueRange);
                points.push(x + ',' + y);
            }}
            
            // 生成平滑曲线路径（使用二次贝塞尔曲线）
            function buildSmoothPath(pts) {{
                if (pts.length < 2) return '';
                var d = 'M ' + pts[0];
                for (var i = 0; i < pts.length - 1; i++) {{
                    var p = pts[i].split(',');
                    var x1 = parseFloat(p[0]);
                    var y1 = parseFloat(p[1]);
                    var p2 = pts[i + 1].split(',');
                    var x2 = parseFloat(p2[0]);
                    var y2 = parseFloat(p2[1]);
                    var mx = (x1 + x2) / 2;
                    var my = (y1 + y2) / 2;
                    d += ' Q ' + x1 + ' ' + y1 + ' ' + mx + ' ' + my;
                }}
                // 直达最后一个点
                d += ' L ' + pts[pts.length - 1];
                return d;
            }}
            var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', buildSmoothPath(points));
            path.setAttribute('stroke', '#007bff');
            path.setAttribute('stroke-width', '3');
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke-linecap', 'round');
            path.setAttribute('stroke-linejoin', 'round');
            svg.appendChild(path);
            
            // 悬浮虚线与提示
            var hoverLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            hoverLine.setAttribute('x1', paddingLeft);
            hoverLine.setAttribute('y1', paddingTop);
            hoverLine.setAttribute('x2', paddingLeft);
            hoverLine.setAttribute('y2', height - paddingBottom);
            hoverLine.setAttribute('stroke', '#999');
            hoverLine.setAttribute('stroke-width', '1.5');
            hoverLine.setAttribute('stroke-dasharray', '5,5');
            hoverLine.style.opacity = 0;
            svg.appendChild(hoverLine);
            
            // 如果有成本价，添加水平虚线
            if (costPrice && costPrice !== 'N/A') {{
                try {{
                    var costValue = parseFloat(costPrice);
                    if (!isNaN(costValue)) {{
                        var costY = paddingTop + ((maxValue - costValue) * chartHeight / valueRange);
                        var costLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        costLine.setAttribute('x1', paddingLeft);
                        costLine.setAttribute('y1', costY);
                        costLine.setAttribute('x2', width - paddingRight);
                        costLine.setAttribute('y2', costY);
                        costLine.setAttribute('stroke', '#ff6b6b');
                        costLine.setAttribute('stroke-width', '2');
                        costLine.setAttribute('stroke-dasharray', '5,5');
                        svg.appendChild(costLine);
                        
                        // 取消右侧成本价文字显示（仅保留虚线与悬浮提示）
                    }}
                }} catch (e) {{
                    console.log('成本价解析失败:', e);
                }}
            }}
            
            // 添加X轴标签（使用抽样后的索引定位）
            for (var i = 0; i < labels.length; i++) {{
                var x = paddingLeft + (labelIndices[i] * chartWidth / (values.length - 1));
                var text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', x);
                text.setAttribute('y', height - paddingBottom + 20);
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('font-size', '12');
                text.setAttribute('fill', '#666');
                text.textContent = labels[i];
                svg.appendChild(text);
            }}
            
            // 曲线下方填充淡蓝色区域
            var areaPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            var areaD = 'M ' + points[0] + ' ';
            var smooth = buildSmoothPath(points);
            areaD += smooth.replace(/^M [^Q]+/, '');
            areaD += ' L ' + points[points.length - 1].split(',')[0] + ',' + (height - paddingBottom) + ' L ' + points[0].split(',')[0] + ',' + (height - paddingBottom) + ' Z';
            areaPath.setAttribute('d', areaD);
            areaPath.setAttribute('fill', 'rgba(0,123,255,0.15)');
            areaPath.setAttribute('stroke', 'none');
            svg.insertBefore(areaPath, path);
            
            // 添加标题
            var title = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            title.setAttribute('x', width / 2);
            title.setAttribute('y', paddingTop - 12);
            title.setAttribute('text-anchor', 'middle');
            title.setAttribute('font-size', '16');
            title.setAttribute('font-weight', 'bold');
            title.setAttribute('fill', '#333');
            title.textContent = titleLabel || '净值走势';
            svg.appendChild(title);

            // 悬浮交互（提示字体更大，成本价与虚线一致颜色）
            svg.addEventListener('mouseleave', function() {{
                hoverLine.style.opacity = 0;
                tooltip.style.display = 'none';
            }});
            svg.addEventListener('mousemove', function(evt) {{
                var rect = svg.getBoundingClientRect();
                var x = evt.clientX - rect.left - 0; // 相对svg左上角
                // 限定到绘图区域
                var cx = Math.max(paddingLeft, Math.min(width - paddingRight, x));
                var ratio = (cx - paddingLeft) / chartWidth;
                // 使用线性插值计算 y 值
                var fIndex = ratio * (values.length - 1);
                var i0 = Math.floor(fIndex);
                var i1 = Math.min(values.length - 1, i0 + 1);
                var t = fIndex - i0;
                var yVal = values[i0] * (1 - t) + values[i1] * t;
                var xPos = cx;
                hoverLine.setAttribute('x1', xPos);
                hoverLine.setAttribute('x2', xPos);
                hoverLine.style.opacity = 1;

                // 取日期标签用最近点索引展示
                var idx = Math.round(fIndex);
                var tip = '日期: ' + data[idx].date + '<br/>单位净值: <b>' + yVal.toFixed(4) + '</b>';
                if (costPrice && costPrice !== 'N/A') {{
                    tip += '<br/>成本单价: <span style="color:#ff6b6b;">' + parseFloat(costPrice).toFixed(4) + '</span>';
                }}
                tooltip.innerHTML = tip;
                tooltip.style.display = 'block';
                tooltip.style.fontSize = '14px';
                // 固定定位：基于视口坐标，垂直居中于绘图区上方，且不被遮挡
                var svgRect = svg.getBoundingClientRect();
                tooltip.style.left = (rect.left + xPos) + 'px';
                tooltip.style.top = (svgRect.top + paddingTop + 50) + 'px';
            }});
            
            // 将SVG添加到容器
            chartContainer.appendChild(svg);
            console.log('SVG图表创建成功');
        }}
    </script>
</body>
</html>"""
    
    # 计算收益颜色类的辅助函数
    def get_profit_color_class_for_table(value_str):
        if value_str == 'N/A':
            return "neutral"
        try:
            # 提取数字部分
            value = float(str(value_str).replace(',', '').replace('¥', '').replace('%', ''))
            if value > 0:
                return "positive"
            elif value < 0:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"
    
    # 生成表格行的函数（用于自选基金，包含持仓信息）
    def generate_table_rows(fund_list):
        rows = ""
        total_today_profit = 0.0
        total_holdings_profit = 0.0
        
        for fund in fund_list:
            change_rate = fund['估算涨跌率']
            try:
                change_value = float(change_rate)
                if change_value > 0:
                    change_class = "positive"
                    change_symbol = "+"
                elif change_value < 0:
                    change_class = "negative"
                    change_symbol = ""
                else:
                    change_class = "neutral"
                    change_symbol = ""
            except:
                change_class = "neutral"
                change_symbol = ""
            
            # 获取持仓信息（如果存在）
            cost_price = fund.get('成本单价', 'N/A')
            today_profit = fund.get('当日收益', 'N/A')
            total_profit = fund.get('持仓收益', 'N/A')
            total_profit_rate = fund.get('持仓收益率', 'N/A')
            
            # 累计收益数据用于汇总行
            if today_profit != 'N/A':
                try:
                    profit_str = str(today_profit).replace('¥', '').replace(',', '')
                    total_today_profit += float(profit_str)
                except:
                    pass
            
            if total_profit != 'N/A':
                try:
                    profit_str = str(total_profit).replace('¥', '').replace(',', '')
                    total_holdings_profit += float(profit_str)
                except:
                    pass
            
            # 格式化日期显示
            jzrq = fund.get('净值日期', '')
            gztime = fund.get('估值时间', '')
            
            # 最新净值显示昨日日期
            latest_date_display = ""
            if jzrq:
                try:
                    # 提取mm-dd格式
                    date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                    latest_date_display = date_obj.strftime('%m-%d')
                except:
                    latest_date_display = jzrq
            
            # 估算净值列标题显示日期，明细行显示时间
            estimate_date_display = ""
            estimate_time_display = ""
            
            # 对于境外基金，使用净值日期显示日期，确保与境外基金tab页一致
            if fund.get('板块分类') == '境外基金':
                # 境外基金：最新净价显示最新净值日期，估值净价显示上日净值日期
                if jzrq and jzrq != 'N/A':
                    try:
                        date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                        latest_date_display = date_obj.strftime('%m-%d')  # 最新净值日期
                    except:
                        latest_date_display = jzrq
                else:
                    latest_date_display = "N/A"
                
                # 估值净价显示上日净值日期
                if gztime and gztime != 'N/A':
                    try:
                        if ' ' in gztime:
                            date_part = gztime.split(' ')[0]
                            date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                            estimate_date_display = date_obj.strftime('%m-%d')
                        else:
                            date_obj = datetime.strptime(gztime, '%Y-%m-%d')
                            estimate_date_display = date_obj.strftime('%m-%d')
                        estimate_time_display = ""  # 境外基金不显示时间
                    except:
                        estimate_date_display = gztime
                        estimate_time_display = ""
                else:
                    estimate_date_display = "N/A"
                    estimate_time_display = ""
            else:
                # 对于其他基金，使用原有的逻辑
                if gztime:
                    try:
                        # 解析估值时间，格式为 "YYYY-MM-DD HH:mm" 或 "HH:mm"
                        if ' ' in gztime:
                            date_part, time_part = gztime.split(' ', 1)
                            date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                            estimate_date_display = date_obj.strftime('%m-%d')
                            estimate_time_display = time_part
                        else:
                            # 如果只有时间部分，使用当前日期
                            estimate_date_display = datetime.now().strftime('%m-%d')
                            estimate_time_display = gztime
                    except:
                        estimate_date_display = datetime.now().strftime('%m-%d')
                        estimate_time_display = ""
                else:
                    estimate_date_display = datetime.now().strftime('%m-%d')
                    estimate_time_display = ""
            
            today_profit_class = get_profit_color_class_for_table(today_profit)
            # 修正：持仓收益与持仓收益率按自身红涨绿跌
            total_profit_class = get_profit_color_class_for_table(total_profit)
            total_profit_rate_class = get_profit_color_class_for_table(total_profit_rate)
            
            rows += f"""
                <tr class="fund-row" ondblclick="showFundDetail('{fund['基金代码']}', '{fund['基金名称']}', '{cost_price}')">
                    <td>{fund['基金代码']}</td>
                    <td>{fund['基金名称']}</td>
                    <td><span class="category-tag category-{fund['板块分类']}">{fund['板块分类']}</span></td>
                    <td>
                        {fund['最新净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{latest_date_display}</div>
                    </td>
                    <td>
                        {fund['估算净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{estimate_date_display if fund.get('板块分类') == '境外基金' else estimate_time_display}</div>
                    </td>
                    <td class="{change_class}">{change_symbol}{change_rate}%</td>
                    <td>{cost_price}</td>
                    <td class="{today_profit_class}">{today_profit}</td>
                    <td class="{total_profit_class}">{total_profit}</td>
                    <td class="{total_profit_rate_class}">{total_profit_rate}</td>
                </tr>"""
        
        # 添加汇总行
        if len(fund_list) > 0:
            # 计算汇总行的CSS类
            today_profit_summary_class = get_profit_color_class_for_table(f"{total_today_profit:,.2f}")
            holdings_profit_summary_class = get_profit_color_class_for_table(f"{total_holdings_profit:,.2f}")
            
            rows += f"""
                <tr style="background-color: #f8f9fa; font-weight: bold;">
                    <td colspan="7" style="text-align: left;">汇总:</td>
                    <td class="{today_profit_summary_class}">{total_today_profit:,.2f}</td>
                    <td class="{holdings_profit_summary_class}">{total_holdings_profit:,.2f}</td>
                    <td>-</td>
                </tr>"""
        
        return rows
    
    # 生成监控基金表格行的函数（不包含持仓信息）
    def generate_monitor_table_rows(fund_list):
        rows = ""
        for fund in fund_list:
            change_rate = fund['估算涨跌率']
            try:
                change_value = float(change_rate)
                if change_value > 0:
                    change_class = "positive"
                    change_symbol = "+"
                elif change_value < 0:
                    change_class = "negative"
                    change_symbol = ""
                else:
                    change_class = "neutral"
                    change_symbol = ""
            except:
                change_class = "neutral"
                change_symbol = ""
            
            # 格式化日期显示
            jzrq = fund.get('净值日期', '')
            gztime = fund.get('估值时间', '')
            
            # 最新净值显示昨日日期
            latest_date_display = ""
            if jzrq:
                try:
                    # 提取mm-dd格式
                    date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                    latest_date_display = date_obj.strftime('%m-%d')
                except:
                    latest_date_display = jzrq
            
            # 估算净值列标题显示日期，明细行显示时间
            estimate_date_display = ""
            estimate_time_display = ""
            if gztime:
                try:
                    # 解析估值时间，格式为 "YYYY-MM-DD HH:mm" 或 "HH:mm"
                    if ' ' in gztime:
                        date_part, time_part = gztime.split(' ', 1)
                        date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                        estimate_date_display = date_obj.strftime('%m-%d')
                        estimate_time_display = time_part
                    else:
                        # 如果只有时间部分，使用当前日期
                        estimate_date_display = datetime.now().strftime('%m-%d')
                        estimate_time_display = gztime
                except:
                    estimate_date_display = datetime.now().strftime('%m-%d')
                    estimate_time_display = ""
            else:
                estimate_date_display = datetime.now().strftime('%m-%d')
                estimate_time_display = ""
            
            rows += f"""
                <tr class="fund-row" ondblclick="showFundDetail('{fund['基金代码']}', '{fund['基金名称']}', 'N/A')">
                    <td>{fund['基金代码']}</td>
                    <td>{fund['基金名称']}</td>
                    <td><span class="category-tag category-{fund['板块分类']}">{fund['板块分类']}</span></td>
                    <td>
                        {fund['最新净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{latest_date_display}</div>
                    </td>
                    <td>
                        {fund['估算净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{estimate_time_display}</div>
                    </td>
                    <td class="{change_class}">{change_symbol}{change_rate}%</td>
                </tr>"""
        return rows
    
    # 生成境外基金表格行的函数（不包含持仓信息，但支持双击绘制图表）
    # 改版：移除"估算净值"，新增"上日净值"，并计算涨跌幅
    def generate_overseas_table_rows(fund_list):
        rows = ""
        
        for fund in fund_list:
            change_rate = fund['估算涨跌率']
            try:
                change_value = float(change_rate)
                if change_value > 0:
                    change_class = "positive"
                    change_symbol = "+"
                elif change_value < 0:
                    change_class = "negative"
                    change_symbol = ""
                else:
                    change_class = "neutral"
                    change_symbol = ""
            except:
                change_class = "neutral"
                change_symbol = ""
            
            # 直接使用基金数据中的日期字段，格式化为MM-dd
            latest_nav_value = fund.get('最新净值', 'N/A')  # 最新净值
            prev_nav_value = fund.get('估算净值', 'N/A')   # 上日净值
            
            # 格式化日期显示
            latest_date_display = ""
            prev_date_display = ""
            
            # 处理净值日期（最新净值日期）
            jzrq = fund.get('净值日期', '')
            if jzrq and jzrq != 'N/A':
                try:
                    date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                    latest_date_display = date_obj.strftime('%m-%d')
                except:
                    latest_date_display = ""
            
            # 处理估值时间（上日净值日期）
            gztime = fund.get('估值时间', '')
            if gztime and gztime != 'N/A':
                try:
                    # 如果估值时间包含日期部分，提取并格式化
                    if ' ' in gztime:
                        date_part = gztime.split(' ')[0]
                        date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                        prev_date_display = date_obj.strftime('%m-%d')
                    else:
                        # 如果只有日期，直接格式化
                        date_obj = datetime.strptime(gztime, '%Y-%m-%d')
                        prev_date_display = date_obj.strftime('%m-%d')
                except:
                    prev_date_display = ""
            
            rows += f"""
                <tr class="fund-row" ondblclick="showFundDetail('{fund['基金代码']}', '{fund['基金名称']}', 'N/A')">
                    <td>{fund['基金代码']}</td>
                    <td>{fund['基金名称']}</td>
                    <td><span class="category-tag category-境外基金">境外基金</span></td>
                    <td>
                        {latest_nav_value}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{latest_date_display}</div>
                    </td>
                    <td>
                        {prev_nav_value}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{prev_date_display}</div>
                    </td>
                    <td class="{change_class}">{change_symbol}{change_rate}%</td>
                </tr>"""
        
        return rows
    
    # 生成场内基金表格行的函数（不包含持仓信息，但支持双击绘制图表）
    def generate_etf_table_rows(fund_list):
        rows = ""
        
        for fund in fund_list:
            change_rate = fund['估算涨跌率']
            try:
                change_value = float(change_rate)
                if change_value > 0:
                    change_class = "positive"
                    change_symbol = "+"
                elif change_value < 0:
                    change_class = "negative"
                    change_symbol = ""
                else:
                    change_class = "neutral"
                    change_symbol = ""
            except:
                change_class = "neutral"
                change_symbol = ""
            
            # ETF基金：最新净价显示当前价格，上日净价显示昨收盘价
            jzrq = fund.get('净值日期', '')
            gztime = fund.get('估值时间', '')
            prev_trade_date = fund.get('昨收盘价日期', '')
            
            # 最新净价显示时间 HH:mm（净价公布时间）
            latest_time_display = ""
            if gztime:
                try:
                    # 解析估值时间，格式为 "YYYY-MM-DD HH:mm" 或 "HH:mm"
                    if ' ' in gztime:
                        time_part = gztime.split(' ', 1)[1]
                        latest_time_display = time_part
                    else:
                        # 如果只有时间部分，直接使用
                        latest_time_display = gztime
                except:
                    latest_time_display = ""
            
            # 上日净价显示日期 MM-DD（昨收盘价日期，即上一交易日）
            prev_date_display = ""
            if prev_trade_date and prev_trade_date != 'N/A':
                try:
                    # 提取mm-dd格式
                    date_obj = datetime.strptime(prev_trade_date, '%Y-%m-%d')
                    prev_date_display = date_obj.strftime('%m-%d')
                except:
                    prev_date_display = prev_trade_date
            elif jzrq:
                try:
                    # 如果没有昨收盘价日期，使用净值日期
                    date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                    prev_date_display = date_obj.strftime('%m-%d')
                except:
                    prev_date_display = jzrq
            
            rows += f"""
                <tr class="fund-row" ondblclick="showFundDetail('{fund['基金代码']}', '{fund['基金名称']}', 'N/A')">
                    <td>{fund['基金代码']}</td>
                    <td>{fund['基金名称']}</td>
                    <td><span class="category-tag category-ETF基金">ETF基金</span></td>
                    <td>
                        {fund['最新净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{latest_time_display}</div>
                    </td>
                    <td>
                        {fund['估算净值']}
                        <div style="font-size: 12px; color: #6c757d; margin-top: 2px;">{prev_date_display}</div>
                    </td>
                    <td class="{change_class}">{change_symbol}{change_rate}%</td>
                </tr>"""
        
        return rows
    
    # 获取各组数据（已按原始定义顺序排序）
    chaochao_data = fund_data_dict.get('chaochao', [])
    yaoyao_data = fund_data_dict.get('yaoyao', [])
    overseas_fund_data = fund_data_dict.get('overseas', [])
    etf_fund_data = fund_data_dict.get('etf', [])
    monitor_data = monitor_funds if monitor_funds else []
    
    # 统计函数
    def compute_stats(fund_list):
        up = down = flat = 0
        total = 0.0
        count = 0
        for fund in fund_list:
            try:
                change_value = float(fund.get('估算涨跌率'))
                total += change_value
                count += 1
                if change_value > 0:
                    up += 1
                elif change_value < 0:
                    down += 1
                else:
                    flat += 1
            except Exception:
                continue
        avg = f"{(total / count):.2f}%" if count > 0 else "0.00%"
        return avg, up, down, flat

    # 各组统计
    avg_change, up_count, down_count, flat_count = compute_stats(monitor_data)
    chaochao_avg_change, chaochao_up_count, chaochao_down_count, chaochao_flat_count = compute_stats(chaochao_data)
    yaoyao_avg_change, yaoyao_up_count, yaoyao_down_count, yaoyao_flat_count = compute_stats(yaoyao_data)
    
    # 计算当日预估收益
    def compute_today_profit(fund_list):
        total_profit = 0.0
        for fund in fund_list:
            try:
                today_profit = fund.get('当日收益', 'N/A')
                if today_profit != 'N/A':
                    # 提取数字部分
                    profit_str = str(today_profit).replace('¥', '').replace(',', '')
                    total_profit += float(profit_str)
            except:
                continue
        return f"{total_profit:,.2f}" if total_profit != 0 else "0.00"
    
    chaochao_today_profit = compute_today_profit(chaochao_data)
    yaoyao_today_profit = compute_today_profit(yaoyao_data)
    
    # 计算收益CSS类
    def get_profit_css_class(profit_str):
        if profit_str == '0.00':
            return 'profit-neutral'
        try:
            profit_value = float(profit_str.replace(',', ''))
            if profit_value > 0:
                return 'profit-positive'
            elif profit_value < 0:
                return 'profit-negative'
            else:
                return 'profit-neutral'
        except:
            return 'profit-neutral'
    
    chaochao_profit_class = get_profit_css_class(chaochao_today_profit)
    yaoyao_profit_class = get_profit_css_class(yaoyao_today_profit)
    
    # 计算平均涨跌率CSS类
    def get_avg_change_css_class(avg_change_str):
        try:
            # 提取数字部分，去掉%符号
            avg_value = float(avg_change_str.replace('%', ''))
            if avg_value > 0:
                return 'positive'
            elif avg_value < 0:
                return 'negative'
            else:
                return 'neutral'
        except:
            return 'neutral'
    
    monitor_avg_class = get_avg_change_css_class(avg_change)
    chaochao_avg_class = get_avg_change_css_class(chaochao_avg_change)
    yaoyao_avg_class = get_avg_change_css_class(yaoyao_avg_change)
    
    # 计算日期标题
    latest_date_header = ""
    estimate_date_header = ""
    
    # 场内基金表头变量
    etf_latest_time_header = ""
    etf_prev_date_header = ""
    
    # 从第一个基金数据中获取日期信息
    if chaochao_data:
        first_fund = chaochao_data[0]
        jzrq = first_fund.get('净值日期', '')
        gztime = first_fund.get('估值时间', '')
        
        # 最新净值标题显示昨日日期
        if jzrq:
            try:
                date_obj = datetime.strptime(jzrq, '%Y-%m-%d')
                latest_date_header = date_obj.strftime('%m-%d')
            except:
                latest_date_header = jzrq
        
        # 估算净值标题显示今日日期
        if gztime:
            try:
                if ' ' in gztime:
                    date_part = gztime.split(' ')[0]
                    date_obj = datetime.strptime(date_part, '%Y-%m-%d')
                    estimate_date_header = date_obj.strftime('%m-%d')
                else:
                    estimate_date_header = datetime.now().strftime('%m-%d')
            except:
                estimate_date_header = datetime.now().strftime('%m-%d')
        else:
            estimate_date_header = datetime.now().strftime('%m-%d')
    
            # 计算ETF基金表头
        if etf_fund_data:
            first_etf = etf_fund_data[0]
            etf_jzrq = first_etf.get('净值日期', '')
            etf_gztime = first_etf.get('估值时间', '')
            etf_prev_trade_date = first_etf.get('昨收盘价日期', '')
            
            # ETF基金最新净价标题显示日期（净价公布日期）
            if etf_jzrq:
                try:
                    date_obj = datetime.strptime(etf_jzrq, '%Y-%m-%d')
                    etf_latest_time_header = date_obj.strftime('%m-%d')
                except:
                    etf_latest_time_header = etf_jzrq
            
            # ETF基金上日净价标题显示日期（昨收盘价日期，即上一交易日）
            if etf_prev_trade_date and etf_prev_trade_date != 'N/A':
                try:
                    date_obj = datetime.strptime(etf_prev_trade_date, '%Y-%m-%d')
                    etf_prev_date_header = date_obj.strftime('%m-%d')
                except:
                    etf_prev_date_header = etf_prev_trade_date
            elif etf_jzrq:
                try:
                    date_obj = datetime.strptime(etf_jzrq, '%Y-%m-%d')
                    etf_prev_date_header = date_obj.strftime('%m-%d')
                except:
                    etf_prev_date_header = etf_jzrq
    
    # 生成HTML文件
    html_content = html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_funds=len(monitor_data),
        chaochao_count=len(chaochao_data),
        yaoyao_count=len(yaoyao_data),
        overseas_count=len(overseas_fund_data),
        monitor_count=len(monitor_data),
        avg_change=avg_change,
        up_count=up_count,
        down_count=down_count,
        flat_count=flat_count,
        chaochao_avg_change=chaochao_avg_change,
        chaochao_up_count=chaochao_up_count,
        chaochao_down_count=chaochao_down_count,
        chaochao_flat_count=chaochao_flat_count,
        yaoyao_avg_change=yaoyao_avg_change,
        yaoyao_up_count=yaoyao_up_count,
        yaoyao_down_count=yaoyao_down_count,
        yaoyao_flat_count=yaoyao_flat_count,
        chaochao_today_profit=chaochao_today_profit,
        yaoyao_today_profit=yaoyao_today_profit,
        chaochao_profit_class=chaochao_profit_class,
        yaoyao_profit_class=yaoyao_profit_class,
        monitor_avg_class=monitor_avg_class,
        chaochao_avg_class=chaochao_avg_class,
        yaoyao_avg_class=yaoyao_avg_class,
        latest_date_header=latest_date_header,
        estimate_date_header=estimate_date_header,
        etf_latest_time_header=etf_latest_time_header,
        etf_prev_date_header=etf_prev_date_header,
        chaochao_table_rows=generate_table_rows(chaochao_data),
        yaoyao_table_rows=generate_table_rows(yaoyao_data),
        monitor_table_rows=generate_monitor_table_rows(monitor_data),
        overseas_table_rows=generate_overseas_table_rows(overseas_fund_data),
        etf_table_rows=generate_etf_table_rows(etf_fund_data)
    )
    
    with open(filename, 'w', encoding='utf-8-sig') as htmlfile:
        htmlfile.write(html_content)
    
    print(f"🌐 HTML: {filename}")
    return filename



def analyze_by_category(fund_data):
    """按板块分析基金表现"""
    if not fund_data:
        return
    
    print("\n=== 板块分析 ===")
    
    # 按板块分组
    category_groups = {}
    for fund in fund_data:
        category = fund['板块分类']
        if category not in category_groups:
            category_groups[category] = []
        category_groups[category].append(fund)
    
    # 分析每个板块
    for category, funds in category_groups.items():
        valid_changes = []
        for fund in funds:
            try:
                change = float(fund['估算涨跌率'])
                valid_changes.append(change)
            except:
                pass
        
        if valid_changes:
            avg_change = sum(valid_changes) / len(valid_changes)
            up_count = len([x for x in valid_changes if x > 0])
            down_count = len([x for x in valid_changes if x < 0])
            
            print(f"🏷️  {category}: {avg_change:+.2f}% (↑{up_count} ↓{down_count})")

def update_github_pages(html_filename):
    """更新GitHub Pages的index.html和.nojekyll文件"""
    try:
        import os
        import subprocess
        
        # 复制最新的HTML文件为index.html
        if os.path.exists(html_filename):
            import shutil
            shutil.copy2(html_filename, 'index.html')
            print(f"✓ 已更新 index.html（从 {html_filename}）")
        
        # 创建.nojekyll文件（如果不存在）
        if not os.path.exists('.nojekyll'):
            with open('.nojekyll', 'w') as f:
                pass
            print("✓ 已创建 .nojekyll 文件")
        
        # 检查是否在git仓库中
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # 在git仓库中，自动提交更新
                subprocess.run(['git', 'add', 'index.html', '.nojekyll'], check=True)
                subprocess.run(['git', 'commit', '-m', f'Update report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'], check=True)
                
                # 尝试推送，如果失败则设置上游分支
                try:
                    try:
                        subprocess.run(['git', 'push'], check=True, timeout=30)
                        print("✓ 已自动推送到GitHub Pages")
                        print("🌐 访问地址: https://SevenKale.github.io/fund-report/")
                    except subprocess.CalledProcessError:
                        # 如果推送失败，尝试设置上游分支
                        try:
                            subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], check=True, timeout=30)
                            print("✓ 已自动推送到GitHub Pages")
                            print("🌐 访问地址: https://SevenKale.github.io/fund-report/")
                        except subprocess.CalledProcessError as e2:
                            print(f"⚠️  Git推送失败: {e2}")
                            print("💡 建议手动推送: git push origin main")
                            print("💡 或检查网络连接后重试")
                except subprocess.TimeoutExpired:
                    print("⚠️  Git推送超时，可能是网络问题")
                    print("💡 建议稍后手动推送: git push origin main")
                except KeyboardInterrupt:
                    print("⚠️  推送被中断（KeyboardInterrupt），已跳过自动推送")
            else:
                print("ℹ️  不在git仓库中，已更新本地文件")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            print("ℹ️  Git未配置或不在仓库中，已更新本地文件")
            
    except Exception as e:
        print(f"⚠️  更新GitHub Pages时出错: {e}")

def update_fund_values():
    """手动更新基金净值（当今日净值公布后）"""
    print("🔄 更新基金净值...")
    print("=" * 50)
    
    # 获取自选基金数据
    print("\n🔍 获取自选基金数据...")
    self_selected_dict = get_self_selected_funds(max_workers=10)
    
    # 获取监控基金数据
    print("\n🔍 获取监控基金数据...")
    monitor_funds = get_monitor_funds(max_workers=10)
    
    if self_selected_dict and monitor_funds:
        # 保存Excel文件（包含多个sheet页）
        excel_filename = save_to_excel(self_selected_dict, monitor_funds)
        # 保存HTML文件（多sheet页显示）
        html_filename = save_to_html_multi_sheet(self_selected_dict, monitor_funds)
        
        print("\n=== 净值更新完成 ===")
        print(f"✅ Excel文件: {excel_filename}")
        print(f"✅ HTML文件: {html_filename}")
        
        # 持仓收益计算
        print("\n=== 持仓收益计算 ===")
        try:
            calculator = HoldingsProfitCalculator()
            holdings_data = calculator.load_holdings_from_excel()
            
            if holdings_data:
                print("💰 计算持仓收益...")
                profit_results = calculator.calculate_holdings_profit(holdings_data, self_selected_dict)
                
                # 显示汇总结果
                print("\n=== 收益汇总 ===")
                for user, result in profit_results.items():
                    user_name = "钞钞" if user == "chaochao" else "垚垚"
                    print(f"\n{user_name}的持仓:")
                    print(f"  总投入: {result['total_cost']:,.2f}")
                    print(f"  当前市值: {result['total_current_value']:,.2f}")
                    print(f"  总收益: {result['total_profit']:,.2f} ({result['total_profit_rate']:+.2f}%)")
                    print(f"  今日收益: {result['today_profit']:,.2f} ({result['today_profit_rate']:+.2f}%)")
                
                print("✅ 持仓收益计算完成")
            else:
                print("⚠️  未能加载持仓数据")
        except Exception as e:
            print(f"⚠️  持仓收益计算失败: {e}")
        
        # 自动更新GitHub Pages
        print("\n=== 自动更新GitHub Pages ===")
        update_github_pages(html_filename)
        
    else:
        print("❌ 未获取到完整的基金数据")

def calculate_holdings_profit():
    """计算持仓收益（独立模式）"""
    print("💰 正在计算持仓收益...")
    print("=" * 60)
    
    # 获取自选基金数据
    print("\n正在获取自选基金数据...")
    self_selected_dict = get_self_selected_funds(max_workers=10)
    
    if not self_selected_dict:
        print("❌ 未能获取到基金数据")
        return
    
    # 计算持仓收益
    print("\n正在计算持仓收益...")
    try:
        calculator = HoldingsProfitCalculator()
        holdings_data = calculator.load_holdings_from_excel()
        
        if not holdings_data:
            print("❌ 未能加载持仓数据")
            return None
        
        profit_results = calculator.calculate_holdings_profit(holdings_data, self_selected_dict)
        
        # 显示汇总结果
        print("\n=== 持仓收益汇总 ===")
        for user, result in profit_results.items():
            user_name = "钞钞" if user == "chaochao" else "垚垚"
            print(f"\n{user_name}的持仓:")
            print(f"  总投入: {result['total_cost']:,.2f}")
            print(f"  当前市值: {result['total_current_value']:,.2f}")
            print(f"  总收益: {result['total_profit']:,.2f} ({result['total_profit_rate']:+.2f}%)")
            print(f"  今日收益: {result['today_profit']:,.2f} ({result['today_profit_rate']:+.2f}%)")
        
        # 保存收益报告
        profit_report_filename = calculator.save_profit_report(profit_results)
        print(f"\n✅ 持仓收益计算完成!")
        print(f"📊 报告文件: {profit_report_filename}")
        
        return profit_results
            
    except Exception as e:
        print(f"❌ 持仓收益计算失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_profit_report(profit_results, filename=None):
    """保存持仓收益报告"""
    if not filename:
        filename = f"持仓收益报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>持仓收益报告</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #333;
            text-align: center;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .profit-positive {
            color: #dc3545;
            font-weight: bold;
        }
        .profit-negative {
            color: #28a745;
            font-weight: bold;
        }
        .profit-neutral {
            color: #6c757d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background-color: white;
        }
        th {
            background-color: #007bff;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
        }
        td {
            padding: 10px 8px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        tr:hover {
            background-color: #e9ecef;
        }
        .timestamp {
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>持仓收益报告</h1>
        <div class="timestamp">生成时间: {timestamp}</div>
        
        {summary_sections}
        
        {detail_sections}
    </div>
</body>
</html>"""
    
    # 生成汇总部分
    summary_sections = ""
    detail_sections = ""
    
    for user, result in profit_results.items():
        user_name = "钞钞" if user == "chaochao" else "垚垚"
        
        # 汇总卡片
        summary_sections += f"""
        <div class="summary-card">
            <h2>{user_name}的持仓汇总</h2>
            <p><strong>总投入:</strong> {result['total_cost']:,.2f}</p>
            <p><strong>当前市值:</strong> {result['total_current_value']:,.2f}</p>
            <p><strong>总收益:</strong> <span class="{'profit-positive' if result['total_profit'] > 0 else 'profit-negative' if result['total_profit'] < 0 else 'profit-neutral'}">{result['total_profit']:,.2f} ({result['total_profit_rate']:+.2f}%)</span></p>
            <p><strong>今日收益:</strong> <span class="{'profit-positive' if result['today_profit'] > 0 else 'profit-negative' if result['today_profit'] < 0 else 'profit-neutral'}">{result['today_profit']:,.2f} ({result['today_profit_rate']:+.2f}%)</span></p>
        </div>
        """
        
        # 详细表格
        detail_sections += f"""
        <h2>{user_name}的持仓明细</h2>
        <table>
            <thead>
                <tr>
                    <th>基金代码</th>
                    <th>基金名称</th>
                    <th>持仓份额</th>
                    <th>成本价</th>
                    <th>当前价格</th>
                    <th>当前市值</th>
                    <th>总收益</th>
                    <th>总收益率</th>
                    <th>今日收益</th>
                    <th>今日涨跌</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for holding in result['holdings']:
            detail_sections += f"""
                <tr>
                    <td>{holding['fund_code']}</td>
                    <td>{holding['fund_name']}</td>
                    <td>{holding['shares']:,.0f}</td>
                    <td>{holding['cost_price']:.4f}</td>
                    <td>{holding['current_price']:.4f}</td>
                    <td>{holding['current_value']:,.2f}</td>
                    <td class="{'profit-positive' if holding['total_profit'] > 0 else 'profit-negative' if holding['total_profit'] < 0 else 'profit-neutral'}">{holding['total_profit']:,.2f}</td>
                    <td class="{'profit-positive' if holding['total_profit_rate'] > 0 else 'profit-negative' if holding['total_profit_rate'] < 0 else 'profit-neutral'}">{holding['total_profit_rate']:+.2f}%</td>
                    <td class="{'profit-positive' if holding['today_profit'] > 0 else 'profit-negative' if holding['today_profit'] < 0 else 'profit-neutral'}">{holding['today_profit']:,.2f}</td>
                    <td class="{'profit-positive' if float(holding['change_rate']) > 0 else 'profit-negative' if float(holding['change_rate']) < 0 else 'profit-neutral'}">{holding['change_rate']}%</td>
                </tr>
            """
        
        detail_sections += """
            </tbody>
        </table>
        """
    
    # 生成HTML文件
    html_content = html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        summary_sections=summary_sections,
        detail_sections=detail_sections
    )
    
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write(html_content)
    
    print(f"✓ 持仓收益报告已保存: {filename}")
    return filename

def main():
    print("=== 基金数据汇总工具 ===")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 检查是否有命令行参数
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--update":
            # 净值更新模式
            update_fund_values()
            return
        elif sys.argv[1] == "--profit":
            # 持仓收益计算模式
            calculate_holdings_profit()
            return
        elif sys.argv[1] == "--help":
            print("使用方法:")
            print("  python combined_fund_tracker.py          # 标准模式：获取基金数据并生成报告")
            print("  python combined_fund_tracker.py --update # 更新模式：更新基金净值")
            print("  python combined_fund_tracker.py --profit # 收益模式：计算持仓收益")
            print("  python combined_fund_tracker.py --help   # 显示帮助信息")
            return
    
    # 可以通过参数调整并发数，默认10个并发
    max_workers = 10
    
    # 获取自选基金数据
    print("\n🔍 获取自选基金数据...")
    self_selected_dict = get_self_selected_funds(max_workers=max_workers)
    
    # 获取监控基金数据
    print("\n🔍 获取监控基金数据...")
    monitor_funds = get_monitor_funds(max_workers=max_workers)
    
    if self_selected_dict and monitor_funds:
        # 加载持仓数据并计算收益（仅用于自选基金，监控基金不显示）
        print("\n💰 加载持仓数据并计算收益...")
        try:
            calculator = HoldingsProfitCalculator()
            holdings_data = calculator.load_holdings_from_excel()
            if holdings_data:
                # 验证持仓数据与基金数据的匹配性
                if not calculator.validate_holdings_data(holdings_data, self_selected_dict):
                    print("⚠️  持仓数据与基金数据不匹配，正在更新持仓数据...")
                    holdings_data = calculator.update_holdings_data()
                
                profit_results = calculator.calculate_holdings_profit(holdings_data, self_selected_dict)
                # 将持仓收益信息添加到基金数据中（仅自选基金）
                self_selected_dict = calculator.enhance_fund_data_with_holdings(self_selected_dict, profit_results)
                print("✅ 持仓信息已添加到自选基金数据中")
            else:
                print("⚠️  未能加载持仓数据")
        except Exception as e:
            print(f"⚠️  加载持仓数据失败: {e}")
        
        # 保存Excel文件（包含多个sheet页）
        excel_filename = save_to_excel(self_selected_dict, monitor_funds)
        # 保存HTML文件（多sheet页显示）
        html_filename = save_to_html_multi_sheet(self_selected_dict, monitor_funds)
        
        print("\n=== 汇总信息 ===")
        
        # 自选基金汇总
        self_selected_total = len(self_selected_dict['all'])
        chaochao_count = len(self_selected_dict.get('chaochao', []))
        yaoyao_count = len(self_selected_dict.get('yaoyao', []))
        
        print(f"📊 自选基金: {self_selected_total} 只 (钞钞: {chaochao_count}, 垚垚: {yaoyao_count})")
        
        # 监控基金汇总
        monitor_total = len(monitor_funds)
        print(f"📊 监控基金: {monitor_total} 只")
        
        # 计算自选基金统计
        self_selected_valid_changes = []
        for fund in self_selected_dict['all']:
            try:
                change = float(fund["估算涨跌率"])
                self_selected_valid_changes.append(change)
            except:
                pass
        
        if self_selected_valid_changes:
            self_selected_avg = sum(self_selected_valid_changes) / len(self_selected_valid_changes)
            self_selected_up = len([x for x in self_selected_valid_changes if x > 0])
            self_selected_down = len([x for x in self_selected_valid_changes if x < 0])
            self_selected_flat = len([x for x in self_selected_valid_changes if x == 0])
            
            print(f"📈 自选基金: {self_selected_avg:+.2f}% (↑{self_selected_up} ↓{self_selected_down} →{self_selected_flat})")
        
        # 计算监控基金统计
        monitor_valid_changes = []
        for fund in monitor_funds:
            try:
                change = float(fund["估算涨跌率"])
                monitor_valid_changes.append(change)
            except:
                pass
        
        if monitor_valid_changes:
            monitor_avg = sum(monitor_valid_changes) / len(monitor_valid_changes)
            monitor_up = len([x for x in monitor_valid_changes if x > 0])
            monitor_down = len([x for x in monitor_valid_changes if x < 0])
            monitor_flat = len([x for x in monitor_valid_changes if x == 0])
            
            print(f"📈 监控基金: {monitor_avg:+.2f}% (↑{monitor_up} ↓{monitor_down} →{monitor_flat})")
        
        # 按板块分析
        analyze_by_category(self_selected_dict['all'])
        print("\n=== 监控基金板块分析 ===")
        analyze_by_category(monitor_funds)
        
        # 持仓收益计算
        print("\n=== 持仓收益计算 ===")
        try:
            calculator = HoldingsProfitCalculator()
            holdings_data = calculator.load_holdings_from_excel()
            
            if holdings_data:
                # 验证持仓数据与基金数据的匹配性
                if not calculator.validate_holdings_data(holdings_data, self_selected_dict):
                    print("⚠️  持仓数据与基金数据不匹配，正在更新持仓数据...")
                    holdings_data = calculator.update_holdings_data()
                
                print("正在计算持仓收益...")
                profit_results = calculator.calculate_holdings_profit(holdings_data, self_selected_dict)
                
                # 显示汇总结果
                print("\n=== 收益汇总 ===")
                for user, result in profit_results.items():
                    user_name = "钞钞" if user == "chaochao" else "垚垚"
                    print(f"\n{user_name}的持仓:")
                    print(f"  总投入: {result['total_cost']:,.2f}")
                    print(f"  当前市值: {result['total_current_value']:,.2f}")
                    print(f"  总收益: {result['total_profit']:,.2f} ({result['total_profit_rate']:+.2f}%)")
                    print(f"  今日收益: {result['today_profit']:,.2f} ({result['today_profit_rate']:+.2f}%)")
                
                print("✅ 持仓收益计算完成")
            else:
                print("⚠️  未能加载持仓数据")
        except Exception as e:
            print(f"⚠️  持仓收益计算失败: {e}")
        
        # 自动更新GitHub Pages
        print("\n=== 自动更新GitHub Pages ===")
        update_github_pages(html_filename)
        
    else:
        print("❌ 未获取到完整的基金数据")

# Flask API服务器 - 用于提供基金历史净值数据
def create_flask_app():
    """创建Flask应用"""
    try:
        from flask import Flask, jsonify, request
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)  # 允许跨域请求
        
        @app.route('/api/fund/history/<fund_code>')
        def get_fund_history(fund_code):
            """获取基金历史净值API端点"""
            try:
                days = request.args.get('days', 7, type=int)
                tracker = OptimizedFundTracker()
                
                # 处理ETF代码和境外基金代码映射
                original_fund_code = fund_code
                processed_fund_code = fund_code
                
                if '.' in fund_code:
                    # 检查是否是ETF代码（以数字开头，以.SZ或.SH结尾）
                    if fund_code.split('.')[0].isdigit() and fund_code.split('.')[1] in ['SZ', 'SH']:
                        # 对于ETF代码，移除交易所后缀
                        base_code = fund_code.split('.')[0]
                        print(f"ETF代码处理: {fund_code} -> {base_code}")
                        processed_fund_code = base_code
                    else:
                        # 对于境外基金代码，使用映射
                        mapped_code = tracker._map_overseas_fund_code(fund_code)
                        if mapped_code:
                            print(f"境外基金代码映射: {fund_code} -> {mapped_code}")
                            processed_fund_code = mapped_code
                
                print(f"最终使用的基金代码: {processed_fund_code}")
                
                data = tracker.get_fund_history_nav(processed_fund_code, days)
                
                if data:
                    return jsonify({
                        'success': True,
                        'fund_code': original_fund_code,
                        'data': data,
                        'count': len(data),
                        'message': f'成功获取{original_fund_code}的历史净值数据'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'fund_code': original_fund_code,
                        'data': [],
                        'count': 0,
                        'message': f'未找到{original_fund_code}的历史净值数据'
                    }), 404
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'fund_code': original_fund_code,
                    'error': str(e),
                    'message': f'获取{original_fund_code}历史净值数据时发生错误'
                }), 500
        
        @app.route('/api/fund/realtime/<fund_code>')
        def get_fund_realtime(fund_code):
            """获取基金实时数据API端点"""
            try:
                tracker = OptimizedFundTracker()
                data = tracker._fetch_single_fund(fund_code)
                
                if data:
                    return jsonify({
                        'success': True,
                        'fund_code': fund_code,
                        'data': data,
                        'message': f'成功获取{fund_code}的实时数据'
                    })
                else:
                    return jsonify({
                        'success': False,
                        'fund_code': fund_code,
                        'data': None,
                        'message': f'未找到{fund_code}的实时数据'
                    }), 404
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'fund_code': fund_code,
                    'error': str(e),
                    'message': f'获取{fund_code}实时数据时发生错误'
                }), 500
        
        @app.route('/api/fund/batch', methods=['POST'])
        def get_batch_fund_data():
            """批量获取基金数据API端点"""
            try:
                data = request.get_json()
                fund_codes = data.get('fund_codes', [])
                
                if not fund_codes:
                    return jsonify({
                        'success': False,
                        'error': '请提供基金代码列表',
                        'message': 'fund_codes参数不能为空'
                    }), 400
                
                tracker = OptimizedFundTracker()
                fund_data = tracker.get_funds_realtime(fund_codes)
                
                return jsonify({
                    'success': True,
                    'fund_codes': fund_codes,
                    'data': fund_data,
                    'count': len(fund_data),
                    'message': f'成功获取{len(fund_data)}只基金的数据'
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'message': '批量获取基金数据时发生错误'
                }), 500
        
        @app.route('/api/health')
        def health_check():
            """健康检查端点"""
            return jsonify({
                'success': True,
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'message': '基金数据API服务运行正常'
            })
        
        return app
        
    except ImportError as e:
        print(f"⚠️  无法创建Flask应用: {e}")
        print("💡 请安装Flask: pip install flask flask-cors")
        return None

def run_api_server(host='127.0.0.1', port=5000, debug=True):
    """运行API服务器"""
    app = create_flask_app()
    if app:
        print(f"🚀 启动基金数据API服务器...")
        print(f"🌐 服务地址: http://{host}:{port}")
        print(f"📊 API端点:")
        print(f"   - GET  /api/fund/history/<fund_code> - 获取基金历史净值")
        print(f"   - GET  /api/fund/realtime/<fund_code> - 获取基金实时数据")
        print(f"   - POST /api/fund/batch - 批量获取基金数据")
        print(f"   - GET  /api/health - 健康检查")
        print(f"💡 按 Ctrl+C 停止服务器")
        
        try:
            app.run(host=host, port=port, debug=debug)
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")
    else:
        print("❌ 无法启动API服务器")

# 如果直接运行此文件且安装了Flask，则启动API服务器
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--api":
            # 启动API服务器模式
            run_api_server()
        elif sys.argv[1] == "--update":
            # 净值更新模式
            update_fund_values()
        elif sys.argv[1] == "--profit":
            # 持仓收益计算模式
            calculate_holdings_profit()
        elif sys.argv[1] == "--help":
            print("使用方法:")
            print("  python combined_fund_tracker.py          # 标准模式：获取基金数据并生成报告")
            print("  python combined_fund_tracker.py --api   # API模式：启动基金数据API服务器")
            print("  python combined_fund_tracker.py --update # 更新模式：更新基金净值")
            print("  python combined_fund_tracker.py --profit # 收益模式：计算持仓收益")
            print("  python combined_fund_tracker.py --help   # 显示帮助信息")
        else:
            main()
    else:
        main()
