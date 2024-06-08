<script>
    /**
     * @type {any[]}
     */
    export let recentFiles = []
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
                        <a class="anchor" href="/encode-picture#file_uuid={row.uuid}">{row.name}</a>
                    </td>
                    <td>{row.type}</td>
                    <td>{row.created_at}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>