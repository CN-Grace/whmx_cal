class Calculater:
    def __init__(self, 属性):
        self.属性 = 属性
        self.伤害类型 = self.属性.伤害类型

    def Calculate_物理伤害(self):
        # 最终伤害 = 当前攻击 × 技能倍率 × (1 - 防御减伤) × 暴击伤害 × 攻击增伤系数 × 受击易伤系数 × (1 - 格挡强度)
        # 防御减伤 = (1-防御穿透) × 当前防御 / (当前防御 + 防御常量)
        # 防御常量 = 400 + 3×受击方等级
        current_attack = self.属性.基础攻击 * (1 + self.属性.百分比攻击力) + self.属性.数值攻击力
        skill_rate = self.属性.常击伤害倍率
        defense_penetration = self.属性.贯穿强度
        defense_constant = 400 + 3 * self.属性.敌方等级
        defense = self.属性.敌方物理防御
        defense_rate = (1 - defense_penetration) * defense / (defense + defense_constant)
        defense_rate = 1 - defense_rate
        critical_damage = self.属性.暴击伤害
        attack_rate = 1 + self.属性.物理伤害提升
        vulnerable_rate = 1 + self.属性.伤害提升
        block_strength = 1 - self.属性.敌方格挡强度
        final_damage = current_attack * skill_rate * defense_rate * critical_damage * attack_rate * vulnerable_rate * block_strength
        return final_damage


if __name__ == "__main__":
    from Model.属性值 import 属性值
    属性 = 属性值()
    属性.基础攻击 = 100
    属性.百分比攻击力 = 0.1
    属性.常击伤害倍率 = 1
    属性.敌方等级 = 100
    属性.敌方物理防御 = 100
    属性.贯穿强度 = 0.7
    属性.暴击伤害 = 1.5
    计算器 = Calculater(属性)
    print(计算器.Calculate_物理伤害())
