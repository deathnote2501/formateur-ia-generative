<script lang="ts">
  import '../app.css'; // Import TailwindCSS styles
  import ChatInterface from '$lib/components/chat/ChatInterface.svelte';
  import SlideNavigation from '$lib/components/slides/SlideNavigation.svelte';
</script>

<div class="min-h-screen flex flex-col">
  <div class="flex-grow flex">
    <main class="flex-grow p-6">
      <slot />
      <SlideNavigation />
    </main>
    <aside class="w-1/3 bg-gray-100 p-4 flex-shrink-0 h-full"> <!-- Added h-full for aside -->
      <ChatInterface />
    </aside>
  </div>
</div>
