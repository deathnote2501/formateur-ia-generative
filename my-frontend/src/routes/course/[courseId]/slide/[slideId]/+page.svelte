<script lang="ts">
  import { page } from '/stores';
  import { currentSlideData, isLoading, fetchSlide, type SlideData } from '/stores/courseStore';

  let title = 'Chargement...';

  $: if (.params.slideId) {
    fetchSlide(.params.slideId);
  }

  $: if (?.content_json?.title) {
    title = .content_json.title;
  } else if (! && !) {
    title = 'Slide non trouvée';
  } else {
    title = 'Plateforme de Formation';
  }
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="slide-content p-4">
  {#if }
    <p class="text-center text-gray-500">Chargement de la slide...</p>
  {:else if }
    <h1 class="text-2xl font-bold mb-3">{.content_json.title}</h1>
    {#if .template_type === 'title' && .content_json.subtitle}
      <p class="text-xl text-gray-700">{.content_json.subtitle}</p>
    {/if}
    {#if .template_type === 'content' && .content_json.elements}
      {#each .content_json.elements as element}
        {#if element.type === 'text'}
          <p class="my-2 text-gray-800">{element.content}</p>
        {/if}
      {/each}
    {/if}
  {:else}
    <p class="text-center text-red-500">Aucune donnée de slide disponible pour l'ID {.params.slideId}.</p>
  {/if}
</div>
