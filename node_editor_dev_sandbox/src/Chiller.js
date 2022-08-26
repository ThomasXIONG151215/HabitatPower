import { Node } from "@baklavajs/core";

export class ChillerNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Chiller";

        this.addOption("设备名称", "InputOption", "冷机");
        this.addOption("冷量输出", "NumberOption", 100);
        this.addOption("传热效率", "NumberOption", 0.8);
        this.addOption("蒸发温度", "NumberOption", 24);

        this.addInputInterface("水流速", "NumberOption", 1);
        this.addInputInterface("冷凝器进水温度", "NumberOption", 10);
        this.addInputInterface("蒸发器进水温度", "NumberOption", 10);

        //this.addOption("Operation", "SelectOption", "Add", undefined, {
        //  items: ["Add", "Subtract"]
        //});
        this.addOutputInterface("冷凝器出水温度", "NumberOption", 22);
        this.addOutputInterface("蒸发器出水温度", "NumberOption", 8);

        this.addOutputInterface("压缩机功率", "NumberOption", 320);
    }

    calculate() {
        const n1 = this.getInterface("水流速").value;
        const n2 = this.getInterface("冷凝器进水温度").value;
        const cold = this.getOptionValue("冷量输出");
        let result;
        result = n1 * n2 * cold;
        this.getInterface("压缩机功率").value = result;
    }
}
