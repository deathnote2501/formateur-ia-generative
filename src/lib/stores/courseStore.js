import { writable } from 'svelte/store';

export const currentSlideData = writable(null);
export const currentSlideId = writable('1');
export const isLoading = writable(false);

export function fetchSlide(slideId) {
  isLoading.set(true);
  setTimeout(() => {
    currentSlideId.set(slideId);
    if (slideId === '1') {
      currentSlideData.set({ template_type: 'title', content_json: { title: 'Bienvenue - Slide 1', subtitle: 'Ceci est la première slide' } });
    } else if (slideId === '2') {
      currentSlideData.set({ template_type: 'content', content_json: { title: 'Contenu - Slide 2', elements: [{ type: 'text', content: 'Voici le contenu de la deuxième slide.' }] } });
    } else if (slideId === '3') {
      currentSlideData.set({ template_type: 'title', content_json: { title: 'Autre Titre - Slide 3', subtitle: 'Contenu du sous-titre pour la slide 3' } });
    } else {
      currentSlideData.set({ template_type: 'content', content_json: { title: `Slide ${slideId}`, elements: [{ type: 'text', content: `Contenu pour la slide ${slideId}` }] } });
    }
    isLoading.set(false);
  }, 300);
}
