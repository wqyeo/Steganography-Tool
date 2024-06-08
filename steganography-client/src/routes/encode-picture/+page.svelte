<script>
	import UseEncodedAsBaseButton from '$lib/components/UseEncodedAsBaseButton.svelte';
	import BitsSelector from '$lib/components/bitsSelector.svelte';
	import EncodingForms from '$lib/components/picture/EncodingForms.svelte';
	import PictureDisplay from '$lib/components/pictureDisplay/SideBySideDisplay.svelte';
	import encodeFile from '$lib/services/encodeFile';
	import { onMount } from 'svelte';

	import { getToastStore } from '@skeletonlabs/skeleton';
	import StartDecodingSelector from '$lib/components/StartDecodingSelector.svelte';

	const toastStore = getToastStore();

	let originalUUID = '31c8b454-feb0-4cc5-b05a-014d3ba96cc4';
	/**
	 * @type {string | null}
	 */
	let encodedUUID = null;

	let redBitsSelection = [0]
	let greenBitsSelection = [0]
	let blueBitsSelection = [0]

	let isEncoding = false;

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

	function useEncodedAsBase() {
		if (encodedUUID == null) {
			console.warn("No Encoded UUID to use as base")
			return
		}

		const fragment = new URLSearchParams(location.hash.slice(1));
		fragment.set('file_uuid', encodedUUID)
		originalUUID = encodedUUID;
		encodedUUID = null;
	}

	/**
	 * @param {string} message
	 * @param {string} secretKey
	 */
	async function sendEncodeRequest(message, secretKey) {
		encodedUUID = null
		isEncoding = true
		const jsonData = await encodeFile(originalUUID, message, redBitsSelection, greenBitsSelection, blueBitsSelection, secretKey);
		isEncoding = false

		const status = jsonData.status
		if (status == "SUCCESS") {
			encodedUUID = jsonData.file_uuid
			return
		}

		let errorMessage = "Unknown error! Try again or submit a Github issue!"
		if (status == "PAYLOAD_TOO_LARGE") {
			errorMessage = "Message is too big to fit into image. Try using more bits or a smaller message!"
		}

		const t = {
			message: errorMessage,
			// Provide any utility or variant background style:
			background: 'variant-filled-warning',
		};
		toastStore.trigger(t)
	}

	/**
	 * @param {boolean} decodeOriginal
	 */
	function startDecoding(decodeOriginal) {
		let fragmentUUID = originalUUID
		if (!decodeOriginal && encodedUUID != null) {
			fragmentUUID = encodedUUID
		}
	}

</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">
		<PictureDisplay bind:originalUUID={originalUUID} bind:comparisonUUID={encodedUUID} />

		<div class="m-2"/>
		<UseEncodedAsBaseButton hasEncodedUUID={encodedUUID != null} onClickCallback={useEncodedAsBase}/>
		<div class="mt-1"/>
		<StartDecodingSelector canDecodeBase={originalUUID != null} canDecodeEncoded={encodedUUID != null} requestDecode={startDecoding}/>

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
		<EncodingForms requestEncode={sendEncodeRequest} disabled={isEncoding}/>
	</div>
</div>

<style>
	.hr {
		width: 95%;
		max-width: 95%;
		margin: 0 auto;
	}
</style>
