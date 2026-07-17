from sqlalchemy import inspect, text

from app.database import engine


TABLE_COLUMNS = {
    "food": [
        ("protein_per_100g", "DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '每100g蛋白质g'"),
        ("fat_per_100g", "DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '每100g脂肪g'"),
        ("fiber_per_100g", "DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '每100g膳食纤维g'"),
        ("sugar_per_100g", "DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '每100g糖g'"),
        ("starch_per_100g", "DECIMAL(5,2) NOT NULL DEFAULT 0 COMMENT '每100g淀粉g'"),
        ("carb_type", "VARCHAR(20) NOT NULL DEFAULT '混合碳' COMMENT '碳水类型'"),
    ],
    "diet_record": [
        ("total_protein", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '总蛋白质g'"),
        ("total_fat", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '总脂肪g'"),
        ("total_fiber", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '总膳食纤维g'"),
        ("fast_carb_total", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '快碳总量g'"),
        ("slow_carb_total", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '慢碳总量g'"),
    ],
    "diet_item": [
        ("protein_value", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '蛋白质估算值g'"),
        ("fat_value", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '脂肪估算值g'"),
        ("fiber_value", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '膳食纤维估算值g'"),
        ("sugar_value", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '糖估算值g'"),
        ("starch_value", "DECIMAL(6,2) NOT NULL DEFAULT 0 COMMENT '淀粉估算值g'"),
        ("carb_type", "VARCHAR(20) NOT NULL DEFAULT '混合碳' COMMENT '碳水类型快照'"),
    ],
    "weekly_report": [
        ("total_protein", "DECIMAL(7,2) NOT NULL DEFAULT 0 COMMENT '总蛋白质g'"),
        ("total_fat", "DECIMAL(7,2) NOT NULL DEFAULT 0 COMMENT '总脂肪g'"),
        ("total_fiber", "DECIMAL(7,2) NOT NULL DEFAULT 0 COMMENT '总膳食纤维g'"),
        ("fast_carb_total", "DECIMAL(7,2) NOT NULL DEFAULT 0 COMMENT '快碳总量g'"),
        ("slow_carb_total", "DECIMAL(7,2) NOT NULL DEFAULT 0 COMMENT '慢碳总量g'"),
    ],
}


FOOD_NUTRITION = [
    ("燕麦", 16.90, 6.90, 10.60, 1.00, 55.90, "慢碳"),
    ("糙米饭", 2.70, 0.90, 1.80, 0.20, 23.80, "慢碳"),
    ("全麦面包", 12.30, 4.20, 6.80, 5.00, 34.00, "慢碳"),
    ("西兰花", 2.80, 0.40, 2.60, 1.70, 1.80, "低碳"),
    ("黄瓜", 0.70, 0.10, 0.50, 1.70, 0.70, "低碳"),
    ("苹果", 0.30, 0.20, 2.40, 10.40, 2.10, "快碳"),
    ("鸡胸肉", 31.00, 3.60, 0.00, 0.00, 0.00, "低碳"),
    ("无糖酸奶", 3.50, 3.20, 0.00, 4.70, 0.30, "混合碳"),
]


def apply_compatible_migrations() -> None:
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())

    with engine.begin() as conn:
        for table, columns in TABLE_COLUMNS.items():
            if table not in table_names:
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            for column_name, definition in columns:
                if column_name not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {definition}"))

        for name, protein, fat, fiber, sugar, starch, carb_type in FOOD_NUTRITION:
            conn.execute(
                text(
                    """
                    UPDATE food
                    SET protein_per_100g = :protein,
                        fat_per_100g = :fat,
                        fiber_per_100g = :fiber,
                        sugar_per_100g = :sugar,
                        starch_per_100g = :starch,
                        carb_type = :carb_type
                    WHERE food_name = :name
                    """
                ),
                {
                    "name": name,
                    "protein": protein,
                    "fat": fat,
                    "fiber": fiber,
                    "sugar": sugar,
                    "starch": starch,
                    "carb_type": carb_type,
                },
            )
