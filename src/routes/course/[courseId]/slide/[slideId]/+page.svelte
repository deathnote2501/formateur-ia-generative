<script>
  import { page } from '$app/stores';
  import { currentSlideData, isLoading, fetchSlide } from '$lib/stores/courseStore.js';

  $: if ($page.params.slideId) {
    fetchSlide($page.params.slideId);
  }
</script>

{#if $isLoading}
  <p>Chargement de la slide...</p>
{:else if $currentSlideData}
  <h1>{$currentSlideData.content_json.title}</h1>
  {#if $currentSlideData.template_type === 'title'}
    <p>{$currentSlideData.content_json.subtitle}</p>
  {:else if $currentSlideData.template_type === 'content' && $currentSlideData.content_json.elements && $currentSlideData.content_json.elements.length > 0}
    <p>{$currentSlideData.content_json.elements[0].content}</p>
  {/if}
{:else}
  <p>Aucune donnée de slide disponible.</p>
{/if}
