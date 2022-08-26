import { Node } from "@baklavajs/core";

export class ExchangerNode extends Node {
    constructor() {
        super();
        this.type = "Device";
        this.name = "Exchanger";
        this.addOption("设备名称", "InputOption", "换热器");
        this.addOption("水泵频率", "NumberOption", 100);
        this.addOption("尺寸", "NumberOption", 24);

        this.addInputInterface("进水流速", "NumberOption", 1);
        this.addInputInterface("进水温度", "NumberOption", 1);
        this.addInputInterface("室内进风流速", "NumberOption", 1);
        this.addInputInterface("室内进风温度", "NumberOption", 1);

        //this.addOption("Operation", "SelectOption", "Add", undefined, {
        //  items: ["Add", "Subtract"]
        //});
        this.addOutputInterface("室内出风温度", "NumberOption", 31);
        this.addOutputInterface("系统出水温度", "NumberOption", 18);

        this.addOutputInterface("水泵功率", "NumberOption", 220);
        this.addOutputInterface("换热量", "NumberOption", 220);
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
