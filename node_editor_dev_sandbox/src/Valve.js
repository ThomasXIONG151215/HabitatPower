import { Node } from "@baklavajs/core";

export class ValveNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Valve";
        this.addOption("设备名称", "InputOption", "节阀");
        this.addOption("开度", "NumberOption", 100);

        this.addInputInterface("进水流速", "NumberOption", 1);
        this.addInputInterface("进水温度", "NumberOption", 1);

        //this.addOption("Operation", "SelectOption", "Add", undefined, {
        //  items: ["Add", "Subtract"]
        //});

        this.addOutputInterface("出水温度", "NumberOption", 18);
    }

    //calculate() {
    //    const n1 = this.getInterface("进水温度").value;
    //    const n2 = this.getInterface("出水温度").value;
    //    const cold = this.getOptionValue("水泵频率");
    //    let result;
    //    result = n1 * n2 * cold;
    //    this.getInterface("泵功率").value = result;
    //}
}
