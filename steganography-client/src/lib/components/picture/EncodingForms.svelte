<script>
	import isWhitespaceOrEmpty from "$lib/isWhitespaceOrEmpty";

    /**
	 * @type {(message: string, keyToUse: string) => void}
	 */
	export let requestEncode;
	export let disabled = false;

    let message = ''
	let keyToUse = "==END=="

	let keyInputClass = 'input';
	let messageInputClass = 'input';
</script>


<label class="label">
	<span class="mr-2">Message</span>
	<textarea class={`${messageInputClass}` + " textarea"} rows="6" placeholder="Message to encode with" bind:value={message} />
</label>

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

<button type="button" disabled={disabled || (isWhitespaceOrEmpty(message) || isWhitespaceOrEmpty(keyToUse))} class="btn variant-filled" on:click={(event) => requestEncode(message, keyToUse)}>
	<span>Encode!</span>
</button>


<style>
	.textarea {
		width: 100%;
		max-width: 100%;
		margin: 0 auto;
	}
</style>