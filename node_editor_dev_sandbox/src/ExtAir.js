import { Node } from "@baklavajs/core";

export class ExtAirNode extends Node {
    constructor() {
        super();
        this.type = "Environment";
        this.name = "ExtAir";
        this.addOption("名称", "InputOption", "室外空气1");

        this.addOutputInterface("温度", "NumberOption", 20);
        this.addOutputInterface("湿度", "NumberOption", 20);
        this.addOutputInterface("风速", "NumberOption", 20);
    }
}
