<script>
	import getApiHttpRoute from "$lib/getApiHttpRoute";

    export const originalUUID = "31c8b454-feb0-4cc5-b05a-014d3ba96cc4"
    /**
     * @type {string | null}
     */
    export const comparisonUUID = null

    console.log(getApiHttpRoute())
</script>

<section class="grid grid-cols-2 md:grid-cols-2 gap-4">
	<div>
        <h2 class="h2">Base Image</h2>
		<img class="mt-2 h-auto max-w-full rounded-lg" src="{getApiHttpRoute()}/download?file_uuid={originalUUID}" alt="">
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