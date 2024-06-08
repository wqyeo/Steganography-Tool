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

<section class="grid grid-cols-2 md:grid-cols-2 gap-4">
	<div>
        <h2 class="h2">Base Image</h2>
        {#if originalUUID != null}
		    <img class="mt-2 h-auto max-w-full rounded-lg" src="{getApiHttpRoute()}/download?file_uuid={originalUUID}" alt="">
        {/if}
	</div>
    <div>
        <h2 class="h2">Encoded Image</h2>
        {#if comparisonUUID != null}
		    <img class="mt-2 h-auto max-w-full rounded-lg" src="{getApiHttpRoute()}/download?file_uuid={comparisonUUID}" alt="">
        {:else}
            <p class="mt-9">Start encoding to compare against something!</p>
        {/if}
    </div>
</section>