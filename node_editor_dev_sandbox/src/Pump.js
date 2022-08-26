import { Node } from "@baklavajs/core";

export class PumpNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Pump";
        this.addOption("水泵频率", "NumberOption", 100);
        this.addOption("尺寸", "NumberOption", 0.8);
        this.addOption("设计流速", "NumberOption", 24);

        this.addInputInterface("进水温度", "NumberOption", 1);

        //this.addOption("Operation", "SelectOption", "Add", undefined, {
        //  items: ["Add", "Subtract"]
        //});
        this.addOutputInterface("出水流速", "NumberOption", 22);
        this.addOutputInterface("出水温度", "NumberOption", 8);

        this.addOutputInterface("泵功率", "NumberOption", 320);
    }

    calculate() {
        const n1 = this.getInterface("进水温度").value;
        const n2 = this.getInterface("出水温度").value;
        const cold = this.getOptionValue("水泵频率");
        let result;
        result = n1 * n2 * cold;
        this.getInterface("泵功率").value = result;
    }
}
