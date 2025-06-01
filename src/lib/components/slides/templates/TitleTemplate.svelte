<script lang="ts">
  export let title: string;
  export let subtitle: string | undefined = undefined;
  export let backgroundImageUrl: string | undefined = undefined;

  $: mainStyle = backgroundImageUrl
    ? `background-image: url('${backgroundImageUrl}'); background-size: cover; background-position: center; color: white; text-shadow: 0 0 8px rgba(0,0,0,0.7);`
    : 'background-color: #f0f0f0; color: #333;';
</script>

<div class="title-template-slide" style="{mainStyle}">
  <div class="overlay" style="{backgroundImageUrl ? 'background-color: rgba(0,0,0,0.4); padding: 2rem; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;' : 'padding: 2rem; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'}">
    <h1>{title}</h1>
    {#if subtitle}
      <p>{subtitle}</p>
    {/if}
  </div>
</div>

<style>
  .title-template-slide {
    width: 100%;
    height: 100%; /* Or a fixed height, depending on layout needs */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
  }

  h1 {
    font-size: 3.5em;
    margin-bottom: 0.25em;
    font-weight: bold;
  }

  p {
    font-size: 1.5em;
    margin-top: 0;
  }
</style>
