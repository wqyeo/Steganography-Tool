<script>
	import BitsSelector from '$lib/components/bitsSelector.svelte';
	import EncodingForms from '$lib/components/picture/EncodingForms.svelte';
	import encodeFile from '$lib/services/encodeFile';
	import { onMount } from 'svelte';

	import { getToastStore } from '@skeletonlabs/skeleton';
	import getApiHttpRoute from '$lib/getApiHttpRoute';
	import DecodingForms from '$lib/components/picture/DecodingForms.svelte';
	import decodeFile from '$lib/services/decodeFile';
	import { goto } from '$app/navigation';
	import GeneratorTypeSelector from '$lib/components/GeneratorTypeSelector.svelte';

	const toastStore = getToastStore();

	let originalUUID = '';

	let redBitsSelection = [7]
	let greenBitsSelection = [7]
	let blueBitsSelection = [7]

	let isDecoding = false;

    const possibleGenerators = ["linear", "fibonacci", "random"];
    let selectedGenerator = "linear";
    
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
		const jsonData = await decodeFile(originalUUID, redBitsSelection, greenBitsSelection, blueBitsSelection, secretKey, selectedGenerator);
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
        goto(`/encode-picture#file_uuid=${originalUUID}`);
    }

</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">

        <img class="mt-2 h-auto max-w-full rounded-lg" src="{getApiHttpRoute()}/download?file_uuid={originalUUID}" alt="">

        <button type="button" class="btn variant-filled mt-2 mb-3" on:click={startEncoding}>Use as Encoding</button>

		<hr class="hr !border-t-4 !border mt-5" />

		<h3 class="h3 mt-2">
			Select Generator
		</h3>
		<GeneratorTypeSelector possibleOptions={possibleGenerators} bind:selectedValue={selectedGenerator}/>
		
		<!--Bits Selection-->
		<h3 class="h3 mt-2">Select Bits</h3>
		<blockquote class="blockquote">By index; 0 is MSB, 7 is LSB</blockquote>
		<ul class="list">
			<li>
				<span class="h6 text-error-600">Red</span>
				<BitsSelector bind:selectedNumbers={redBitsSelection}/>
			</li>
			<li>
				<span class="h6 text-secondary-600">Blue</span>
				<BitsSelector bind:selectedNumbers={blueBitsSelection}/>
			</li>
			<li>
				<span class="h6 text-success-600">Green</span>
				<BitsSelector bind:selectedNumbers={greenBitsSelection}/>
			</li>
		</ul>

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
