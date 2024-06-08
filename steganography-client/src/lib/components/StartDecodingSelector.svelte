<script>
    /**
     * @type {(decodeBase: boolean) => void}
    */
    export let requestDecode;

    export let canDecodeBase = true
    export let canDecodeEncoded = false
</script>

<div class="btn-group variant-filled">
	<button disabled={!canDecodeBase} on:click={(e) => requestDecode(true)}>Decode Base</button>
	<button disabled={!canDecodeEncoded} on:click={(e) => requestDecode(false)}>Decode Encoded</button>
</div>