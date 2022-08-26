<template>
    <div style="height: 100vh; width: 100vw">
        <hint-overlay />
        <baklava-editor :plugin="viewPlugin" />
    </div>
</template>

<script>
import HintOverlay from "./HintOverlay.vue";
import { Editor } from "@baklavajs/core";
import { ViewPlugin } from "@baklavajs/plugin-renderer-vue";
import { OptionPlugin } from "@baklavajs/plugin-options-vue";
import { Engine } from "@baklavajs/plugin-engine";
import { MathNode } from "./MathNode";
import { DisplayNode } from "./DisplayNode";
import { ChillerNode } from "./Chiller";
import { PumpNode } from "./Pump";
import { AssemblerNode } from "./Assembler";
import { EnveloppeNode } from "./Enveloppe";
import { SpaceNode } from "./Space";
import { MeterNode } from "./Meter";
import { SunNode } from "./Sun";
import { ValveNode } from "./Valve";
import { TowerNode } from "./Tower";

export default {
    components: { HintOverlay },
    data() {
        return {
            editor: new Editor(),
            viewPlugin: new ViewPlugin(),
            engine: new Engine(true)
        };
    },
    created() {
        // Register the plugins
        // The view plugin is used for rendering the nodes
        this.editor.use(this.viewPlugin);
        // The option plugin provides some default option UI elements
        this.editor.use(new OptionPlugin());
        // The engine plugin calculates the nodes in the graph in the
        // correct order using the "calculate" methods of the nodes
        this.editor.use(this.engine);

        // Show a minimap in the top right corner
        this.viewPlugin.enableMinimap = true;

        // register the nodes we have defined, so they can be
        // added by the user as well as saved & loaded.
        this.editor.registerNodeType("MathNode", MathNode);
        this.editor.registerNodeType("DisplayNode", DisplayNode);
        this.editor.registerNodeType("Chiller", ChillerNode);
        this.editor.registerNodeType("Pump", PumpNode);
        this.editor.registerNodeType("Assembler", AssemblerNode);
        this.editor.registerNodeType("Enveloppe", EnveloppeNode);
        this.editor.registerNodeType("Space", SpaceNode);
        this.editor.registerNodeType("Sun", SunNode);
        this.editor.registerNodeType("Meter", MeterNode);
        this.editor.registerNodeType("Valve", ValveNode);
        this.editor.registerNodeType("Tower", TowerNode);

        // add some nodes so the screen is not empty on startup
        const node1 = this.addNodeWithCoordinates(ChillerNode, 100, 140);
        const node2 = this.addNodeWithCoordinates(PumpNode, 400, 140);

        //this.editor.addConnection(
        //    node1.getInterface("Result"),
        //    node2.getInterface("Value")
        //);
        this.engine.calculate();
    },
    methods: {
        addNodeWithCoordinates(nodeType, x, y) {
            const n = new nodeType();
            this.editor.addNode(n);
            n.position.x = x;
            n.position.y = y;
            return n;
        }
    }
};
</script>