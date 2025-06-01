<script lang="ts">
  import "../app.css"; // Import Tailwind CSS global styles
  import ChatInterface from "$lib/components/chat/ChatInterface.svelte";
  import SlideNavigation from "$lib/components/slides/SlideNavigation.svelte";
</script>

<div class="flex h-screen">
  <aside class="w-1/4 h-full border-r bg-gray-50">
    <ChatInterface />
  </aside>
  <main class="flex-1 flex flex-col h-full overflow-y-auto">
    <div class="flex-grow p-4">
      <slot />
    </div>
    <SlideNavigation />
  </main>
</div>

<style>
  /* You can add any additional global styles specific to the layout here if needed,
     but prefer Tailwind classes for general styling. */
</style>
