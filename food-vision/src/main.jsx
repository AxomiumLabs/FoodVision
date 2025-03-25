import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ChakraProvider, CSSReset } from '@chakra-ui/react'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ChakraProvider>
      <CSSReset />
      <App />
    </ChakraProvider>
  </StrictMode>,
)
