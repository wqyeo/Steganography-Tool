<script>
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

	/**
	 * @type {FileList}
	 */
	let files;

	let uploadingFile = false;
	let uploadedFile = false;
	let fileUUID = '';

	let modeIsEncoding = true;
	let encodedFileUUID = '';

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
			fileUUID = encodeResult.uuid;
			uploadedFile = true;
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

	const getFileUrl = (/** @type {string} */ uuid) => {
		const baseApiUrl = getApiHttpRoute();
		console.log(`Getting image of ${uuid}`);
		return `${baseApiUrl}/get-uploaded-file/${uuid}`;
	};

	const getEncodedFileUrl = (/** @type {any} */ uuid, /** @type {any} */ encodedUUID) => {
		const baseApiUrl = getApiHttpRoute();
		return `${baseApiUrl}/get-encoded-file/${uuid}/${encodedUUID}`;
	};

	let showingEncodedFile = false;

	/**
	 * @param {Event} event
	 */
	function toggle(event) {
		// @ts-ignore
		showingEncodedFile = event.target.checked;
	}

	let selectedRedBits = [0];
	let selectedGreenBits = [1];
	let selectedBlueBits = [1];

	let toEncode = '';
	let keyToUse = '==END==';

	let isEncoding = false;
	let hasEncoded = false;

	let encodingInputClass = 'input';
	let keyInputClass = 'input';
	let showKeyCollisionError = false;

	let decodedMessage = ""
	let keyUsedSuccessfully = false

	async function triggerDecode() {
		//#region Form Validation
		let hasError = false
		keyInputClass = 'input';

		if (keyToUse.trim() == '') {
			keyInputClass = 'input-warning';
			hasError = true
		}

		if (
			selectedBlueBits.length === 0 &&
			selectedRedBits.length === 0 &&
			selectedGreenBits.length === 0
		) {
			const t = {
				message: 'Select bits to use first!',
				background: 'variant-filled-warning'
			};
			toastStore.trigger(t);
			hasError = true;
		}

		if (hasError) {
			return;
		}
		//#endregion
		
		isEncoding = true;
		const response = await decodeFile(
			fileUUID,
			selectedRedBits,
			selectedGreenBits,
			selectedBlueBits,
			keyToUse
		)
		isEncoding = false

		if (response.status == "SUCCESS") {
			decodedMessage = response.decoded
			keyUsedSuccessfully = (response.found == true || response.found.toString() == "true")

			if (decodedMessage == ""){
				decodedMessage = "No message has been found!"
			}
			return
		}

		const t = {
			message: 'Unknown error, contact admin or try again!',
			background: 'variant-filled-error'
		};
		toastStore.trigger(t);
	}

	async function triggerEncode() {
		//#region Form Validation
		encodingInputClass = 'input';
		keyInputClass = 'input';
		showKeyCollisionError = false;
		let hasError = false;

		if (toEncode.trim() == '') {
			encodingInputClass = 'input-warning';
			hasError = true
		}

		if (keyToUse.trim() == '') {
			keyInputClass = 'input-warning';
			hasError = true
		}

		if (toEncode.includes(keyToUse)) {
			keyInputClass = 'input-error';
			showKeyCollisionError = true;
			hasError = true
		}

		if (
			selectedBlueBits.length === 0 &&
			selectedRedBits.length === 0 &&
			selectedGreenBits.length === 0
		) {
			const t = {
				message: 'Select bits to use first!',
				background: 'variant-filled-warning'
			};
			toastStore.trigger(t);
			hasError = true;
		}

		if (hasError) {
			return;
		}
		//#endregion
		isEncoding = true;

		const response = await encodeFile(
			fileUUID,
			toEncode,
			selectedRedBits,
			selectedGreenBits,
			selectedBlueBits,
			keyToUse
		);

		isEncoding = false;
		if (response.status == 'SUCCESS') {
			hasEncoded = true;
			encodedFileUUID = response.uuid;
			return;
		}

		if (response.status == 'PAYLOAD_TOO_LARGE') {
			const t = {
				message: 'Message is too large to fit into image! Try another image or reduce message.',
				background: 'variant-filled-warning'
			};
			toastStore.trigger(t);
		} else {
			const t = {
				message: 'Unknown error, try again later!',
				background: 'variant-filled-error'
			};
			toastStore.trigger(t);
		}

		hasEncoded = false;
		showingEncodedFile = false;
	}
</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-4 text-center flex flex-col items-center take-viewport">
		{#if !uploadedFile}
			<UploadFile files={files} onFileUploadedHandler={onFileUploadedHandler}/>
		{:else if uploadingFile}
			<div class="ProgressRadialWrapper">
				<ProgressRadial value={undefined} />
			</div>
		{:else if uploadedFile}
			<!--Show original image based on switch-->
			<!--Original image is always shown when decoding (Decoding is based on original image only...)-->
			{#if showingEncodedFile && modeIsEncoding}
				<img src={getEncodedFileUrl(fileUUID, encodedFileUUID)} alt="Encoded File" />
			{:else}
				<img src={getFileUrl(fileUUID)} alt="Original File" />
			{/if}

			<button 
			type="button" 
			class="btn variant-filled-warning"
			on:click={(ee) => {
				fileUUID="";
				encodedFileUUID=""
				showingEncodedFile=false
				uploadedFile=false
				modeIsEncoding=false
				hasEncoded=false
				files=null
			}}
			disabled={isEncoding}
			>
				<span>
					<Icon icon="icon-park-outline:clear" />
				</span>
				<span>
					Clear File
				</span>
			</button>

			{#if !modeIsEncoding}
				<blockquote class="blockquote">
					Decoding based on the original uploaded file!
					Only supports ASCII Encoded Messages!
				</blockquote>
			{/if}

			<!--Toggle switch between decoding or encoding..-->
			<RadioGroup disabled={isEncoding} active="variant-filled-primary" hover="hover:variant-soft-primary">
				<RadioItem bind:group={modeIsEncoding} name="justify" value={true}>Encode</RadioItem>
				<RadioItem bind:group={modeIsEncoding} name="justify" value={false}>Decode</RadioItem>
			</RadioGroup>

			{#if modeIsEncoding}
				<!--ENCODE :: Toggle to see original image vs encoded image. (Usable if had encoded.)-->
				<SlideToggle
					name="slider-label"
					on:change={toggle}
					bind:checked={showingEncodedFile}
					disabled={!hasEncoded}
				>
					{showingEncodedFile ? 'Showing Encoded' : 'Showing Original'}
				</SlideToggle>

				<!--Bit selection tickboxes-->
				<h4 class="h4">Select Bits to use</h4>
				<h4 class="h6 ">Red</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedRedBits} />
				<h4 class="h6">Green</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedGreenBits} />
				<h4 class="h6">Blue</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedBlueBits} />

				<!--Message and Key input-->
				<label class="label">
					<span class="mr-2">Message</span>
					<input
						class={`${encodingInputClass}`}
						title="Text to Encode"
						type="text"
						placeholder="Text to encode..."
						bind:value={toEncode}
					/>
				</label>

				<label class="label">
					<span class="mr-2">End Key</span>
					<input
						class={`${keyInputClass}`}
						title="Ending Code (key)"
						type="text"
						placeholder="Unique ending code to use"
						bind:value={keyToUse}
					/>
				</label>

				{#if showKeyCollisionError}
					<p>Key should not be a part of the message!!</p>
				{/if}

				<!--Send-->
				<button
					type="button"
					class="btn variant-filled"
					on:click={(e) => triggerEncode()}
					disabled={isEncoding}
				>
					{#if isEncoding}
						<span>
							<Icon icon="line-md:loading-twotone-loop" />
						</span>
					{:else}
						<span>
							<Icon icon="ph:file-lock-fill" />
						</span>
					{/if}
					<span>Encode!</span>
				</button>
			{:else}
				<!--DECODE :: Bit selection-->
				<h4 class="h4">Select Bits to use</h4>
				<h4 class="h6">Red</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedRedBits} />
				<h4 class="h6">Green</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedGreenBits} />
				<h4 class="h6">Blue</h4>
				<BitSelectionGroup bind:selectedNumbers={selectedBlueBits} />

				<!--Key to use-->
				<label class="label">
					<span class="mr-2">End Key</span>
					<input
						class={`${keyInputClass}`}
						title="Ending Code (key)"
						type="text"
						placeholder="Unique ending code to use"
						bind:value={keyToUse}
					/>
				</label>

				<!--Send-->
				<button
					type="button"
					class="btn variant-filled"
					on:click={(e) => triggerDecode()}
					disabled={isEncoding}
				>
					{#if isEncoding}
						<span>
							<Icon icon="line-md:loading-twotone-loop" />
						</span>
					{:else}
						<span>
							<Icon icon="hugeicons:file-unlocked" />
						</span>
					{/if}
					<span>Decode!</span>
				</button>

				<!--Show decoded message, and key usage status-->
				{#if decodedMessage}
					{#if keyUsedSuccessfully}
						<blockquote class="blockquote">
							Key was successfully used!
						</blockquote>
					{:else}
						<blockquote class="blockquote">
							Failed to use key!
						</blockquote>
					{/if}
					<h5 class="h5">Decoded Message</h5>
					<pre class="pre decoded-message">{decodedMessage}</pre>
				{/if}
			{/if}
		{/if}
	</div>
</div>

<style>
	.input {
		width: 50vw;
	}

	.decoded-message {
		width: 75vw;
	}

	.input-warning {
		width: 50vw;
	}

	.input-error {
		width: 50vw;
	}

	.take-viewport {
		width: 100vw;
	}

	.tickboxes {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		margin-top: 16px;
	}

	.small-mr {
		margin-right: 6px;
	}

	.tickbox {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-right: 6px;
	}

	.tickbox:last-child {
		margin-right: 0;
	}

	.tickbox input {
		margin-bottom: 2px;
	}
</style>
