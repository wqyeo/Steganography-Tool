<script>
    export let selectedNumbers = [7];

	/**
	 *
	 * @param {number} number
	 */
	function toggleNumber(number) {
		const index = selectedNumbers.indexOf(number);
		if (index === -1) {
			selectedNumbers = [...selectedNumbers, number];
		} else {
			selectedNumbers.splice(index, 1);
			selectedNumbers = [...selectedNumbers];
		}

		console.debug(selectedNumbers);
	}
</script>

<div class="tickboxes">
    {#each Array.from({ length: 8 }, (_, i) => i) as number}
        <div class="tickbox">
            <input
                type="checkbox"
                class="checkbox"
                on:change={() => toggleNumber(number)}
                checked={selectedNumbers.includes(number)}
                id={`checkbox-${number}`}
            />
            <label for={`checkbox-${number}`}>{number}</label>
        </div>
    {/each}
</div>

<style>
.tickboxes {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 16px;
}

.tickbox {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-right: 6px;
}

.tickbox:last-child {
    margin-right: 0;
}

.tickbox input {
    margin-bottom: 2px;
}
</style>