<script>
	import BitsSelector from '$lib/components/bitsSelector.svelte';
	import EncodingForms from '$lib/components/picture/EncodingForms.svelte';
	import encodeFile from '$lib/services/encodeFile';
	import { onMount } from 'svelte';

	import { RangeSlider, getToastStore } from '@skeletonlabs/skeleton';
	import getApiHttpRoute from '$lib/getApiHttpRoute';
	import DecodingForms from '$lib/components/picture/DecodingForms.svelte';
	import decodeFile from '$lib/services/decodeFile';
	import { goto } from '$app/navigation';
	import decodeAudio from '$lib/services/decodeAudio';

	const toastStore = getToastStore();

	let originalUUID = '';

	let lsbSelection = 0;
	let isDecoding = false;

    let decoded = false;
    let keySuccess = false;
    let decodedMessage = ""

	onMount(() => {
		// Get the file_uuid from the URL fragment
		const fragment = new URLSearchParams(location.hash.slice(1));
		const uuid = fragment.get('file_uuid');
		if (uuid == null) {
			console.warn("UUID in fragment header not set!")
			originalUUID = '31c8b454-feb0-4cc5-b05a-014d3ba96cc4';
			return
		}

		originalUUID = uuid;
	});

	/**
	 * @param {string} secretKey
	 */
	async function sendDecodeRequest(secretKey) {
        decoded = false
		isDecoding = true
		const jsonData = await decodeAudio(originalUUID, lsbSelection, secretKey);
		isDecoding = false

		const status = jsonData.status
		if (status == "SUCCESS") {
			keySuccess = (jsonData.found == true || jsonData.found.toString() == "true")
            decodedMessage = jsonData.decoded
            decoded = true
			return
		}

		let errorMessage = "Unknown error! Try again or submit a Github issue!"
		const t = {
			message: errorMessage,
			// Provide any utility or variant background style:
			background: 'variant-filled-warning',
		};
		toastStore.trigger(t)
	}


    function startEncoding(){
        goto(`/encode-audio#file_uuid=${originalUUID}`);
    }

</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">

		<audio controls>
			<source src="{getApiHttpRoute()}/download?file_uuid={originalUUID}">
			Your browser does not support the audio element.
		</audio>

        <button type="button" class="btn variant-filled mt-2 mb-3" on:click={startEncoding}>Use as Encoding</button>

		<hr class="hr !border-t-4 !border mt-5" />

		<!--Bits Selection-->
		<h3 class="h3 mt-2">Select LSB Bits</h3>
		<RangeSlider name="range-slider" bind:value={lsbSelection} max={7} step={1} ticked>{lsbSelection}</RangeSlider>

		<hr class="hr !border-t-4 !border mt-5" />
		<h3 class="h3 mt-2">Set Keys</h3>
		<DecodingForms requestDecode={sendDecodeRequest} disabled={isDecoding}/>

        {#if decoded}
		    <hr class="hr !border-t-4 !border mt-5" />

            {#if keySuccess}
		        <h3 class="h3 mt-2 text-success-500">Key used successfully!</h3>
            {:else}
		        <h3 class="h3 mt-2 text-warning-500">Failed to use key!</h3>
            {/if}

            <pre class="pre decoded-message">{decodedMessage}</pre>
        {/if}
        

	</div>
</div>

<style>
    .decoded-message {
		width: 75vw;
	}

	.hr {
		width: 95%;
		max-width: 95%;
		margin: 0 auto;
	}
</style>
