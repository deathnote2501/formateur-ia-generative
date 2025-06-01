<script>
  import { goto } from '$app/navigation';
  import { currentSlideId } from '$lib/stores/courseStore.js';

  function goToNextSlide() {
    const nextSlideId = String(Number($currentSlideId) + 1);
    goto(`/course/1/slide/\${nextSlideId}`);
  }

  function goToPrevSlide() {
    const prevSlideId = Math.max(1, Number($currentSlideId) - 1);
    goto(`/course/1/slide/\${prevSlideId}`);
  }
</script>

<nav>
  <button on:click={goToPrevSlide} disabled={Number($currentSlideId) <= 1}>Précédent</button>
  <button on:click={goToNextSlide}>Suivant</button>
</nav>

<style>
  nav {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
  }
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
  }
</style>
