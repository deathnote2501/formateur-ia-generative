<script lang="ts">
  import TitleTemplate from './templates/TitleTemplate.svelte';
  import MenuTemplate from './templates/MenuTemplate.svelte';
  import ContentTemplate from './templates/ContentTemplate.svelte';

  export let slideData: {
    template_type: string;
    content_json: any; // This will be spread into the respective components
    // Other slide properties might exist but are not directly used by SlideViewer
  } | null | undefined;

</script>

<div class="slide-viewer-container">
  {#if !slideData || !slideData.template_type}
    <p>Données de slide invalides ou template non spécifié.</p>
  {:else if slideData.template_type === 'title'}
    <TitleTemplate {...slideData.content_json} />
  {:else if slideData.template_type === 'menu'}
    <MenuTemplate {...slideData.content_json} />
  {:else if slideData.template_type === 'content'}
    <ContentTemplate {...slideData.content_json} />
  {:else}
    <p>Template de slide inconnu: {slideData.template_type}</p>
  {/if}
</div>

<style>
  .slide-viewer-container {
    width: 100%;
    height: 100%; /* Ensure it fills its parent, or set specific dimensions */
    display: flex; /* Optional: if you want to center content or manage layout directly */
    justify-content: center; /* Optional: centers content if it's smaller than container */
    align-items: center; /* Optional: centers content vertically */
  }

  /* Ensure that the templates themselves define their sizing and internal layout */
  .slide-viewer-container > :global(div) { /* Targets the root div of each template */
    width: 100%;
    height: 100%;
  }

  p { /* Styling for error messages */
    font-size: 1.2em;
    color: red;
    text-align: center;
    padding: 2rem;
  }
</style>
