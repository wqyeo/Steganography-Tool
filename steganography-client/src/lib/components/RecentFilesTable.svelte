<script>
    /**
     * @type {any[]}
     */
    export let recentFiles = []

    import { goto } from '$app/navigation';

    // @ts-ignore
    function handleNavigation(row) {
        const newFragment = `#file_uuid=${row.uuid}`;
        const currentUrl = window.location.href;

        console.log(currentUrl)

        let urlRoute = ''
        if (row.type == "image/png") {
            urlRoute = "encode-picture"
        } else if (row.type == "audio/x-wav" || row.type == "audio/wav") {
            urlRoute = "encode-audio"
        }

        if (currentUrl.includes(urlRoute)) {
            location.hash = newFragment;
            location.reload();
        } else {
            goto(`/${urlRoute}${newFragment}`);
        }
    }
</script>

<div class="table-container">
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            {#each recentFiles as row, i}
                <tr>
                    <td>
                        <button on:click={(e) => handleNavigation(row)} class="button">
                            <div class="text-tertiary-500">
                                {row.name}
                            </div>
                        </button>
                    </td>
                    <td>{row.type}</td>
                    <td>{row.created_at}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>