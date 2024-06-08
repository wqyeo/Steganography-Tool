<script>
	// NOTE: Upload page...
	import { getToastStore } from '@skeletonlabs/skeleton';

	const toastStore = getToastStore();

	import getApiHttpRoute from '$lib/getApiHttpRoute';
	import encodeFile from '$lib/services/encodeFile';
	import uploadForEncode from '$lib/services/uploadForEncode';
	import Icon from '@iconify/svelte';

	import { RadioGroup, RadioItem } from '@skeletonlabs/skeleton';

	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { SlideToggle } from '@skeletonlabs/skeleton';
	import BitSelectionGroup from '$lib/components/bitsSelector.svelte';
	import decodeFile from '$lib/services/decodeFile';
	import UploadFile from '$lib/components/uploadFile/UploadFile.svelte';
	import { goto } from '$app/navigation';
	import RecentFilesTable from '$lib/components/RecentFilesTable.svelte';
	import { onMount } from 'svelte';
	import fetchRecentFiles from '$lib/services/fetchRecentFiles';

	/**
	 * @type {FileList}
	 */
	let files;

	let uploadingFile = false;
	let uploadedFile = false;
	let fileUUID = '';

	/**
	 * @param {Event} e
	 */
	async function onFileUploadedHandler(e) {
		uploadingFile = true;
		uploadedFile = false;

		// @ts-ignore
		const encodeResult = await uploadForEncode(files.item(0));
		uploadingFile = false;

		if (encodeResult.status == 'SUCCESS') {
			fileUUID = encodeResult.file_uuid;
			uploadedFile = true;
			if (encodeResult.type.startsWith("image")) {
				goto(`/encode-picture#file_uuid=${fileUUID}`);
			} else {
				console.warn(`No page created for uploaded file of type ${encodeResult.type}`)
			}
			return;
		}

		if (encodeResult.status == 'SIZE_EXCEED') {
			const t = {
				message: 'File is too big! (Max 512KiB)',
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
		} else if (encodeResult.status == 'BAD_TYPE') {
			const t = {
				message: 'Invalid file type!',
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
		} else {
			const t = {
				message: 'Unknown error, try again later!',
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
		}

		console.error(encodeResult.message);
	}

	/**
	 * @type {any[]}
	 */
	let recentFiles = []
	onMount(() => {
		fetchRecentFiles().then((jsonData) => {
			if (jsonData.status == "SUCCESS") {
				recentFiles = jsonData.data;
			}
		})
	})
</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport" style="width: 95vh;">
		{#if !uploadingFile}
			<UploadFile bind:files={files} onFileUploadedHandler={onFileUploadedHandler}/>
		{:else}
			<div class="ProgressRadialWrapper">
				<ProgressRadial value={undefined} />
			</div>
		{/if}

		{#if recentFiles.length >= 1}
			<hr class="hr !border-t-4 !border mt-5" />
			<h3 class="h3 mt-2 mb-3">Recently Uploaded Files</h3>
			<RecentFilesTable bind:recentFiles={recentFiles}/>
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