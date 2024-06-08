<script>
    export let onClickCallback;
    export let hasEncodedUUID = false;
</script>

<button type="button" disabled={!hasEncodedUUID} class="btn variant-filled" on:click={onClickCallback}>Use Encoded as Base</button>