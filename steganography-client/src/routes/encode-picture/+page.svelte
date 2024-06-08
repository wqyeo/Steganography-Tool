<script>
	import UseEncodedAsBaseButton from '$lib/components/UseEncodedAsBaseButton.svelte';
	import BitsSelector from '$lib/components/bitsSelector.svelte';
	import EncodingForms from '$lib/components/picture/EncodingForms.svelte';
	import PictureDisplay from '$lib/components/pictureDisplay/PictureDisplay.svelte';
	import { onMount } from 'svelte';
  	import { writable } from 'svelte/store';

	let originalUUID = '';
	let encodedUUID = null;

	let redBitsSelection = [0]
	let greenBitsSelection = [0]
	let blueBitsSelection = [0]

	onMount(() => {
		// Get the file_uuid from the URL fragment
		const fragment = new URLSearchParams(location.hash.slice(1));
		const uuid = fragment.get('file_uuid');
		if (uuid == null) {
			console.warn("UUID in fragment header not set!")
			return
		}

		originalUUID = uuid;
	});

	function useEncodedAsBase(){

	}

	/**
	 * @param {string} message
	 * @param {string} secretKey
	 */
	function sendEncodeRequest(message, secretKey) {

	}


</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">
		<PictureDisplay />
		<div class="m-4"/>
		<UseEncodedAsBaseButton hasEncodedUUID={encodedUUID != null} onClickCallback={useEncodedAsBase}/>

		<hr class="hr !border-t-4 !border mt-5" />

		<!--Bits Selection-->
		<h3 class="h3 mt-2">Select Bits</h3>
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
		<h3 class="h3 mt-2">Set Message and Keys</h3>
		<EncodingForms requestEncode={sendEncodeRequest}/>
	</div>
</div>

<style>
	.hr {
		width: 95%;
		max-width: 95%;
		margin: 0 auto;
	}
</style>
