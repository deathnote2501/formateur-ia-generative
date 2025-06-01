<script lang="ts">
  import { page } from '$app/stores';
  import { courseStore, type SlideData } from '$lib/stores/courseStore'; // Assuming courseStore path
  import SlideViewer from '$lib/components/slides/SlideViewer.svelte'; // Import SlideViewer
  import { onMount } from 'svelte';

  let currentSlideData: SlideData | null = null;
  let isLoading = true;
  let errorMessage: string | null = null;

  // Subscribe to route parameters
  $: courseId = $page.params.courseId;
  $: slideId = $page.params.slideId;

  // Fetch slide data when parameters change
  $: {
    if (courseId && slideId) {
      loadSlideData(courseId, slideId);
    }
  }

  async function loadSlideData(cId: string, sId: string) {
    isLoading = true;
    errorMessage = null;
    currentSlideData = null; // Clear previous slide data
    try {
      // Attempt to fetch from store; store handles actual fetching or mock data
      await courseStore.fetchSlide(cId, sId);
      // The store itself updates $currentSlideData, so we subscribe to that
    } catch (error) {
      if (error instanceof Error) {
        errorMessage = `Erreur lors du chargement de la slide : ${error.message}`;
      } else {
        errorMessage = 'Erreur lors du chargement de la slide.';
      }
      console.error(error);
    } finally {
      isLoading = false;
    }
  }

  // Subscribe to the store's currentSlideData
  // Assuming courseStore exposes currentSlideData as a readable store
  const unsubscribe = courseStore.currentSlideData.subscribe(value => {
    currentSlideData = value;
  });

  onMount(() => {
    // Initial load based on current params
    if (courseId && slideId) {
      loadSlideData(courseId, slideId);
    }
    return () => {
      // Cleanup subscription when component is destroyed
      if (unsubscribe) {
        unsubscribe();
      }
    };
  });

</script>

<div class="slide-page-container">
  {#if isLoading}
    <p>Chargement de la slide...</p>
  {:else if errorMessage}
    <p style="color: red;">{errorMessage}</p>
  {:else if currentSlideData}
    <!-- Replace direct data display with SlideViewer -->
    <SlideViewer slideData={currentSlideData} />
  {:else}
    <p>Aucune donnée de slide disponible pour {courseId} / {slideId}.</p>
  {/if}
</div>

<style>
  .slide-page-container {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #eee; /* A light background for the page */
  }

  /* Ensure SlideViewer's container or the templates themselves handle specific slide appearance */
  /* Basic loading/error message styling */
  p {
    font-size: 1.2em;
    color: #333;
  }
</style>
