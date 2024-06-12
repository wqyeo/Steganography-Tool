<script>
	import { RadioGroup, RadioItem } from "@skeletonlabs/skeleton";

    export const possibleOptions = ["linear", "fibonacci", "random"];
    export let selectedValue = "linear";
</script>

<RadioGroup>
    {#each possibleOptions as option}
        <RadioItem bind:group={selectedValue} name="justify" value={option}>{option}</RadioItem>
    {/each}
</RadioGroup>
