import { writable } from 'svelte/store';

// Define a type for SlideData (can be expanded)
/**
 * @typedef {Object} SlideData
 * @property {string} id
 * @property {string} template_type
 * @property {object} content_json
 * @property {string | undefined} [notes]
 */

/**
 * @typedef {Object} MenuItem
 * @property {string} id
 * @property {string} text
 * @property {string | number} targetSlideId
 */

/**
 * @typedef {Object} ContentElement
 * @property {string} type
 * @property {string} [text] - For subtitle
 * @property {string} [content] - For text (HTML)
 * @property {boolean} [ordered] - For list
 * @property {string[]} [items] - For list
 * @property {string} [url] - For image/video
 * @property {string} [caption] - For image/video
 */


// Writable store for the current slide's data
const _currentSlideData = writable(null);

// Mock database of slides
const mockSlides = {
  '1': {
    id: '1',
    template_type: 'title',
    content_json: {
      title: 'Bienvenue au Cours de Svelte!',
      subtitle: 'Une introduction interactive',
      backgroundImageUrl: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80' // Example image
    },
    notes: 'Ceci est la première slide du cours.'
  },
  '2': {
    id: '2',
    template_type: 'menu',
    content_json: {
      title: 'Menu Principal',
      subtitle: 'Choisissez une section à explorer :',
      menuItems: [
        { id: 's1-intro', text: 'Introduction (Slide 1)', targetSlideId: '1' },
        { id: 's1-content', text: 'Contenu Détaillé (Slide 3)', targetSlideId: '3' },
        { id: 's1-conclusion', text: 'Autre Menu (Slide 4)', targetSlideId: '4' }
      ]
    },
    notes: 'Menu pour naviguer dans le cours.'
  },
  '3': {
    id: '3',
    template_type: 'content',
    content_json: {
      title: 'Les Bases de Svelte',
      elements: [
        { type: 'subtitle', text: 'Réactivité' },
        { type: 'text', content: 'Svelte est un compilateur qui transforme vos composants en code JavaScript impératif très efficace. <strong>Ceci est important!</strong>' },
        { type: 'list', ordered: false, items: ['Pas de DOM virtuel', 'Moins de code boilerplate', 'Vraiment réactif'] },
        { type: 'image', url: 'https://svelte.dev/svelte-logo-horizontal.svg', caption: 'Logo Svelte' },
        // { type: 'video', url: 'https://www.youtube.com/embed/somevideoID', caption: 'Vidéo de présentation Svelte' } // Example video
      ]
    },
    notes: 'Slide de contenu avec divers éléments.'
  },
  '4': {
    id: '4',
    template_type: 'menu',
    content_json: {
      title: 'Menu Secondaire',
      menuItems: [
        { id: 's4-back', text: 'Retour au Menu Principal (Slide 2)', targetSlideId: '2'},
        { id: 's4-start', text: 'Retour à l\'accueil (Slide 1)', targetSlideId: '1'}
      ]
    }
  }
};

// Function to simulate fetching slide data
async function fetchSlide(courseId, slideId) {
  console.log(`Fetching slide for course ${courseId}, slide ${slideId}`);
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const slideKey = String(slideId); // Ensure slideId is a string for lookup
      if (mockSlides[slideKey]) {
        _currentSlideData.set(mockSlides[slideKey]);
        resolve(mockSlides[slideKey]);
      } else {
        _currentSlideData.set(null);
        reject(new Error(`Slide with ID ${slideId} not found for course ${courseId}.`));
      }
    }, 500); // Simulate network delay
  });
}

export const courseStore = {
  fetchSlide,
  currentSlideData: {
    subscribe: _currentSlideData.subscribe
  }
  // you might add other store methods or properties here
};

// Export types if needed by other modules, though JSDoc is used here for type hints
// export { SlideData, MenuItem, ContentElement };
