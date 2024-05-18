<script>
	import Icon from '@iconify/svelte';

	import { ProgressRadial } from '@skeletonlabs/skeleton';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { SlideToggle } from '@skeletonlabs/skeleton';

	/**
	 * @type {FileList}
	 */
	let files;

	/**
	 * @param {Event} e
	 */
	function onFileUploadedHandler(e) {
		console.debug('file data:', e);
	}

	let isChecked = false;

	/**
	 * @param {Event} event
	 */
	function toggle(event) {
		// @ts-ignore
		isChecked = event.target.checked;
	}

	/**
	 * @type {number[]}
	 */
	let selectedNumbers = [0];

	/**
	 *
	 * @param {number} number
	 */
	function toggleNumber(number) {
		const index = selectedNumbers.indexOf(number);
		if (index === -1) {
			selectedNumbers = [...selectedNumbers, number];
		} else {
			selectedNumbers.splice(index, 1);
			selectedNumbers = [...selectedNumbers];
		}

		console.debug(selectedNumbers);
	}

	let toEncode = '';

	let isEncoding = false;
	let hasEncoded = false;

	let encodingInputClass = "input"

	function triggerEncode() {
		if (toEncode.trim() == "") {
			encodingInputClass = "input-warning"
			return
		} else {
			encodingInputClass = "input"
		}

		isEncoding = true;
		// TODO: Invoke backend API
	}
</script>

<div class="container h-full mx-auto flex justify-center mt-9">
	<div class="space-y-10 text-center flex flex-col items-center take-viewport">
		{#if files == undefined || files == null}
			<FileDropzone name="files" bind:files on:change={onFileUploadedHandler}>
				<svelte:fragment slot="lead">
					<Icon icon="line-md:upload-loop" width="192" height="192" />
				</svelte:fragment>
				<svelte:fragment slot="message">
					<b>Upload a file</b> or drag and drop
				</svelte:fragment>
				<svelte:fragment slot="meta">10MB Max. PNG allowed.</svelte:fragment>
			</FileDropzone>
		{:else}
			<div class="ProgressRadialWrapper">
				<ProgressRadial value={undefined} />
			</div>
			<SlideToggle
				name="slider-label"
				on:change={toggle}
				bind:checked={isChecked}
				disabled={!hasEncoded}
			>
				{isChecked ? 'Showing Encoded' : 'Showing Original'}
			</SlideToggle>

			<!--Bit selection tickboxes-->
			<h4 class="h4">Select Bits to use</h4>
			<div class="tickboxes">
				{#each Array.from({ length: 8 }, (_, i) => i).reverse() as number}
					<div class="tickbox">
						<input
							type="checkbox"
							class="checkbox"
							on:change={() => toggleNumber(number)}
							checked={selectedNumbers.includes(number)}
							id={`checkbox-${number}`}
						/>
						<label for={`checkbox-${number}`}>{number}</label>
					</div>
				{/each}
			</div>

			<input
				class={`${encodingInputClass}`}
				title="Text to Encode"
				type="text"
				placeholder="Text to encode..."
				bind:value={toEncode}
			/>
			<button type="button" class="btn variant-filled" on:click={(e) => triggerEncode()} disabled={isEncoding}>
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
		{/if}
	</div>
</div>

<style>
	.input {
		width: 50vw;
	}

	.input-warning {
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
