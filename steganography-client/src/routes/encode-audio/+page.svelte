<script>
	import UseEncodedAsBaseButton from '$lib/components/UseEncodedAsBaseButton.svelte';
	import BitsSelector from '$lib/components/bitsSelector.svelte';
	import EncodingForms from '$lib/components/picture/EncodingForms.svelte';
	import PictureDisplay from '$lib/components/pictureDisplay/SideBySideDisplay.svelte';
	import encodeFile from '$lib/services/encodeFile';
	import { onMount } from 'svelte';

	import { RangeSlider, getToastStore } from '@skeletonlabs/skeleton';
	import StartDecodingSelector from '$lib/components/StartDecodingSelector.svelte';
	import { goto } from '$app/navigation';
	import fetchRelatedFiles from '$lib/services/fetchRelatedFiles';
	import RelatedFilesTable from '$lib/components/RelatedFilesTable.svelte'
	import SideBySidePlayer from '$lib/components/audioDisplay/SideBySidePlayer.svelte';
	import encodeAudio from '$lib/services/encodeAudio';

	const toastStore = getToastStore();

	let originalUUID = '';
	/**
	 * @type {string | null}
	 */
	let encodedUUID = null;

	let lsbSelection = 0;
	let isEncoding = false;

	/**
	 * @type {any[]}
	 */
	let relatedFiles = []

	onMount(() => {
		// Get the file_uuid from the URL fragment
		const fragment = new URLSearchParams(location.hash.slice(1));
		const uuid = fragment.get('file_uuid');
		if (uuid == null) {
			console.warn("UUID in fragment header not set!")
			goto("/")
			return
		}

		originalUUID = uuid;
		fetchRelatedFiles(uuid).then((jsonData) => {
			if (jsonData.status == "SUCCESS") {
				relatedFiles = jsonData.data 
			}
		})
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
		const jsonData = await encodeAudio(originalUUID, message, lsbSelection, secretKey);
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

		goto(`/decode-audio#file_uuid=${fragmentUUID}`);
	}

</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">
		<SideBySidePlayer originalUUID={originalUUID} comparisonUUID={encodedUUID}/>

		<div class="m-2"/>
		<UseEncodedAsBaseButton hasEncodedUUID={encodedUUID != null} onClickCallback={useEncodedAsBase}/>
		<div class="mt-1"/>
		<StartDecodingSelector canDecodeBase={originalUUID != null} canDecodeEncoded={encodedUUID != null} requestDecode={startDecoding}/>

		<hr class="hr !border-t-4 !border mt-5" />

		<!--Bits Selection-->
		<h3 class="h3 mt-2">Select LSB Bits</h3>
		<RangeSlider name="range-slider" bind:value={lsbSelection} max={7} step={1} ticked>LSB Select</RangeSlider>

		<hr class="hr !border-t-4 !border mt-5" />
		<h3 class="h3 mt-2">Set Message and Keys</h3>
		<EncodingForms requestEncode={sendEncodeRequest} disabled={isEncoding}/>

		{#if relatedFiles.length >= 1}
			<hr class="hr !border-t-4 !border mt-5" />
			<h3 class="h3 mt-2 mb-3">Related Files</h3>
			<RelatedFilesTable bind:relatedFiles={relatedFiles}/>
		{/if}
	</div>
</div>

<style>
	.hr {
		width: 95%;
		max-width: 95%;
		margin: 0 auto;
	}
</style>
