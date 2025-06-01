<script lang="ts">
  import '../app.css'; // Import TailwindCSS styles
</script>

<div class="min-h-screen flex flex-col">
  <div class="flex-grow flex">
    <main class="flex-grow p-6">
      <slot />
    </main>
    <aside class="w-1/3 bg-gray-100 p-4 flex-shrink-0">
      <!-- Ensure this sidebar does not shrink by adding flex-shrink-0 -->
      <p>Sidebar Chat</p>
    </aside>
  </div>
</div>
