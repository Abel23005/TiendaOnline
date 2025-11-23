import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from './client';

export function useProducts() {
  return useQuery({
    queryKey: ['productos'],
    queryFn: async () => {
      const { data } = await api.get('/api/productos/');
      return data;
    },
  });
}

export function useProduct(id) {
  return useQuery({
    queryKey: ['producto', id],
    queryFn: async () => {
      const { data } = await api.get(`/api/productos/${id}/`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCategories() {
  return useQuery({
    queryKey: ['categorias'],
    queryFn: async () => {
      const { data } = await api.get('/api/categorias/');
      return data;
    },
  });
}

export function useProductsByCategory(id) {
  return useQuery({
    queryKey: ['productosPorCategoria', id],
    queryFn: async () => {
      const { data } = await api.get(`/api/categorias/${id}/productos/`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCart() {
  return useQuery({
    queryKey: ['cart'],
    queryFn: async () => {
      const { data } = await api.get('/api/cart/');
      return data;
    },
  });
}

export function useAddToCart() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ productoId, cantidad }) =>
      api.post('/api/cart/', { producto_id: productoId, cantidad }),
    onMutate: async ({ productoId, cantidad }) => {
      await queryClient.cancelQueries({ queryKey: ['cart'] });
      const previousCart = queryClient.getQueryData(['cart']);

      queryClient.setQueryData(['cart'], (old) => {
        if (!old) {
          return {
            items: [],
            total_items: 0,
            subtotal: 0,
          };
        }
        const items = [...old.items];
        const index = items.findIndex((i) => i.producto.id === productoId);
        if (index !== -1) {
          const item = items[index];
          const nuevaCantidad = item.cantidad + cantidad;
          items[index] = {
            ...item,
            cantidad: nuevaCantidad,
            subtotal: Number(item.producto.precio) * nuevaCantidad,
          };
        }
        return {
          ...old,
          items,
          total_items: items.length,
          subtotal: items.reduce((acc, it) => acc + Number(it.subtotal), 0),
        };
      });

      return { previousCart };
    },
    onError: (_error, _variables, context) => {
      if (context?.previousCart) {
        queryClient.setQueryData(['cart'], context.previousCart);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}

export function useUpdateCartItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ itemId, cantidad }) =>
      api.patch(`/api/cart/${itemId}/`, { cantidad }),
    onMutate: async ({ itemId, cantidad }) => {
      await queryClient.cancelQueries({ queryKey: ['cart'] });
      const previousCart = queryClient.getQueryData(['cart']);

      queryClient.setQueryData(['cart'], (old) => {
        if (!old) return old;
        const items = old.items.map((item) =>
          item.id === itemId
            ? {
                ...item,
                cantidad,
                subtotal: Number(item.producto.precio) * cantidad,
              }
            : item,
        );
        return {
          ...old,
          items,
          subtotal: items.reduce((acc, it) => acc + Number(it.subtotal), 0),
        };
      });

      return { previousCart };
    },
    onError: (_error, _variables, context) => {
      if (context?.previousCart) {
        queryClient.setQueryData(['cart'], context.previousCart);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}

export function useRemoveCartItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (itemId) => api.delete(`/api/cart/${itemId}/`),
    onMutate: async (itemId) => {
      await queryClient.cancelQueries({ queryKey: ['cart'] });
      const previousCart = queryClient.getQueryData(['cart']);

      queryClient.setQueryData(['cart'], (old) => {
        if (!old) return old;
        const items = old.items.filter((item) => item.id !== itemId);
        return {
          ...old,
          items,
          total_items: items.length,
          subtotal: items.reduce((acc, it) => acc + Number(it.subtotal), 0),
        };
      });

      return { previousCart };
    },
    onError: (_error, _variables, context) => {
      if (context?.previousCart) {
        queryClient.setQueryData(['cart'], context.previousCart);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });
}
