import csv

# 定义标签体系
tag_system = {
    "主题标签": {
        "历史文化": ["南宋御街", "德寿宫遗址", "凤山水城门", "胡庆余堂", "岳王庙"],
        "名人故居": ["郁达夫故居", "章太炎故居", "苏东坡纪念馆", "龚自珍故居"],
        "民俗文化": ["小河直街", "塘栖古镇",  "西塘古镇"],
        "现代建筑": ["杭州国际会议中心", "杭州奥体中心", "来福士中心"],
        "溜娃路线": ["少年宫", "博物院", "动物园", "水族馆"],
        "自然景观": ["西湖", "西溪湿地", "千岛湖", "莫干山"],
        "夜景与夜市": ["夜宵", "夜市", "夜景", "灯光秀"],
        "宗教文化": ["灵隐寺", "净慈寺", "法喜寺", "抱朴道院"],
        "艺术与博物馆": ["浙江美术馆", "中国丝绸博物馆", "浙江省博物馆", "良渚博物院"]
    },
    "场景标签": {
        "Citywalk 路线": ["徒步路线", "一日游路线", "文化探索路线", "城市漫步路线"],
        "打卡地点": ["小众打卡", "必打卡", "拍照打卡", "网红打卡", "情侣打卡"],
        "文化体验场所": ["传统技艺体验", "民俗文化体验", "艺术文化体验", "历史文化体验"],
        "户外自然场景": ["山林徒步场景", "滨水休闲场景", "郊野露营场景", "自然观赏场景"],
        "夜间场景": ["夜景观赏", "夜市体验", "夜间娱乐", "夜间休闲"],
        "宗教场所": ["佛教寺院", "道教宫观", "基督教教堂", "伊斯兰教清真寺"],
        "创意园区": ["艺术创意园区", "文化创意园区", "科技创意园区", "时尚创意园区"],
         "运动健身场所": ["健身房", "游泳馆", "瑜伽馆", "羽毛球馆", "乒乓球馆", "篮球场","足球场","台球","保龄球", "登山步道", "骑行绿道"],
    },
    "受众标签": {
        "亲子家庭": ["亲子", "儿童", "全家一起"],
        "老年群体": ["老年","休闲", "康养", "慢节奏"],
        "商务人士": [ "会议","会展", "高端商务"],
        "宠物爱好者": ["狗", "宠物活动", "猫"],
        "情侣": ["约会", "情侣", "甜蜜","浪漫"],
        "学生党": ["校园", "学生", "青春"],
        "游客": ["热门景点", "旅游攻略", "特色纪念品"],
    },
     "特殊兴趣标签": {
        "美食探索": ["美食", "餐厅", "美味", "小吃","吃喝"],
        "拍照打卡": ["摄影", "拍照", "打卡", "机位"],
        "休闲娱乐": ["放松", "娱乐","社交","聚会"],
        "购物消费": ["购物中心", "特色街区", "品牌", "特产"],
        "徒步": ["徒步", "户外"],
        "音乐爱好": ["演出", "工作室", "音乐节", "演唱会","live house"],
    },
    "时间标签": {
        "四季": ["春", "夏", "秋", "冬"],
        "日间": ["白天", "日间", "上午", "下午"],
        "夜间": ["夜间", "夜景", "夜市", "夜晚"],
        "全天": ["24小时", "全天候", "全天开放"],
        "节日": ["春节", "国庆", "中秋", "端午"],
        "周末": ["周末", "周六", "周日"],
        "寒暑假": ["暑假", "寒假", "假期"]
    }
}

# 初始化分类字典，每个标签对应一个空列表
classified_data = {}
for main_tag, sub_tags in tag_system.items():
    for sub_tag, keywords in sub_tags.items():
        for keyword in keywords:
            classified_data[keyword] = []

# 读取 CSV 文件
try:
    with open('qwen_cleaned_notes.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # 获取 CSV 文件的字段名
        fieldnames = reader.fieldnames
        # 添加一个新的字段用于存储标签
        fieldnames.append('标签')
        for row in reader:
            # 处理 None 值，将其转换为空字符串
            values = [str(value) if value is not None else '' for value in row.values()]
            # 将每一行数据转换为字符串
            row_str = ' '.join(values)
            tagged = False
            for main_tag, sub_tags in tag_system.items():
                for sub_tag, keywords in sub_tags.items():
                    for keyword in keywords:
                        if keyword in row_str:
                            # 如果包含关键字，则将该行数据添加到相应的分类列表中
                            new_row = row.copy()
                            new_row['标签'] = f"{main_tag}-{sub_tag}-{keyword}"
                            classified_data[keyword].append(new_row)
                            tagged = True
            if not tagged:
                # 如果没有匹配到任何标签，标记为未分类
                new_row = row.copy()
                new_row['标签'] = '未分类'
                classified_data.setdefault('未分类', []).append(new_row)

    # 输出分类结果到一个新的 CSV 文件
    filename = 'classified_data.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data_list in classified_data.values():
            for row in data_list:
                writer.writerow(row)
    print(f"分类结果已保存到 {filename}")

except FileNotFoundError:
    print("未找到 'qwen_cleaned_notes.csv' 文件，请检查文件路径。")