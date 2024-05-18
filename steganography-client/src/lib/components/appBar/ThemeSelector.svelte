<script>
	// @ts-nocheck
	import { SlideToggle, popup, ListBox, ListBoxItem, LightSwitch } from '@skeletonlabs/skeleton';
	import themes from '$lib/themes.json';

	import Icon from '@iconify/svelte';

	import { get } from 'svelte/store';
	import { themePreference } from '$lib/store/themePreference';

	let selectedTheme = get(themePreference);

	const themePopupSetting = {
		event: 'click',
		target: 'themePopup',
		placement: 'bottom'
	};

	function onNewThemeSelected(newTheme) {
		themePreference.set(newTheme);
		document.body.setAttribute('data-theme', newTheme);
	}
</script>

<!--Theme Selection Button-->
<button type="button" class="btn varient-filled ml-2" use:popup={themePopupSetting}>
	<div class="theme-dropdown-button">
		Theme
		<Icon icon="gridicons:dropdown" />
	</div>
</button>

<!--Popup for selecting a theme-->
<div class="card p-4 w-72 shadow-xl" data-popup="themePopup">
	<div class="mode-selector">
		<div>Mode</div>
		<LightSwitch />
	</div>
	<hr class="m-4 !border-t-4" />

	<ListBox>
		{#each themes as { name, value }}
			<ListBoxItem
				bind:group={selectedTheme}
				name="themes"
				{value}
				on:change={() => onNewThemeSelected(value)}
			>
				{name}
			</ListBoxItem>
		{/each}
	</ListBox>

	<div class="arrow bg-surface-100-800-token" />
</div>

<style>
	.theme-dropdown-button {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.mode-selector {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
</style>
