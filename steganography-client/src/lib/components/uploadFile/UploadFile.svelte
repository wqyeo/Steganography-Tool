<script>
	import Icon from "@iconify/svelte";
	import { FileDropzone } from "@skeletonlabs/skeleton";

	/**
	 * @type {FileList}
	 */
    export let files;
    export let onFileUploadedHandler;
</script>

<FileDropzone name="files" bind:files on:change={onFileUploadedHandler}>
    <svelte:fragment slot="lead">
        <Icon icon="line-md:upload-loop" width="192" height="192" />
    </svelte:fragment>
    <svelte:fragment slot="message">
        <b>Upload a file</b> or drag and drop
    </svelte:fragment>
    <svelte:fragment slot="meta">
        <b>2MB Max</b>
        <p>PNG, WAV allowed</p>
    </svelte:fragment>
</FileDropzone>