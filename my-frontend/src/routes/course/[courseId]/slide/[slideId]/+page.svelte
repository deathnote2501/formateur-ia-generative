<script lang="ts">
  import { page } from '$app/stores';
  import { currentSlideData, isLoading, fetchSlide, type SlideData } from '$lib/stores/courseStore';
  import SlideViewer from '$lib/components/slides/SlideViewer.svelte'; // New import

  let title = 'Chargement...';

  $: if ($page.params.slideId) {
    fetchSlide($page.params.slideId);
  }

  $: if ($currentSlideData?.content_json?.title) {
    title = $currentSlideData.content_json.title;
  } else if (!$isLoading && !$currentSlideData) {
    title = 'Slide non trouvée';
  } else {
    title = 'Plateforme de Formation';
  }
</script>

<svelte:head>
  <title>{title}</title>
</svelte:head>

<div class="slide-content w-full h-full"> <!-- Ensure this container allows SlideViewer to take space -->
  {#if $isLoading}
    <p class="text-center text-gray-500 py-10">Chargement de la slide...</p>
  {:else if $currentSlideData}
    <SlideViewer slideData={$currentSlideData} />
  {:else}
    <p class="text-center text-red-500 py-10">Aucune donnée de slide disponible pour l'ID {$page.params.slideId}.</p>
  {/if}
</div>
