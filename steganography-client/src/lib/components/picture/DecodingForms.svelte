<script>
	import isWhitespaceOrEmpty from "$lib/isWhitespaceOrEmpty";

    /**
	 * @type {(keyToUse: string) => void}
	 */
	export let requestDecode;
	export let disabled = false;

	let keyToUse = "==END=="
	let keyInputClass = 'input';
</script>

<label class="label">
	<span class="mr-2">Secret Key</span>
	<input
		class={`${keyInputClass}`}
		title="Ending Code (key)"
		type="text"
		placeholder="Unique ending code to use"
		bind:value={keyToUse}
	/>
</label>

<button type="button" disabled={disabled || isWhitespaceOrEmpty(keyToUse)} class="btn variant-filled" on:click={(event) => 	requestDecode(keyToUse)}>
	<span>Encode!</span>
</button>


<style>
	.textarea {
		width: 100%;
		max-width: 100%;
		margin: 0 auto;
	}
</style>