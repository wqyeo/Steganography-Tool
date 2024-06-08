<script>
	import getApiHttpRoute from "$lib/getApiHttpRoute";

    /**
     * @type {string | null}
     */
    export let originalUUID = null;
    /**
     * @type {string | null}
     */
    export let comparisonUUID = null;
</script>

	<div>
        <h2 class="h2">Base Audio</h2>
        {#if originalUUID != null}
            <audio controls>
                <source src="{getApiHttpRoute()}/download?file_uuid={originalUUID}">
                Your browser does not support the audio element.
            </audio>
        {/if}
	</div>
    <div>
        <h2 class="h2">Encoded Audio</h2>
        {#if comparisonUUID != null}
            <audio controls>
                <source src="{getApiHttpRoute()}/download?file_uuid={comparisonUUID}">
                Your browser does not support the audio element.
            </audio>
        {:else}
            <p class="mt-9">Start encoding to compare against something!</p>
        {/if}
    </div>