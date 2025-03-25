import { useState } from 'react'
import { Box, VStack, HStack, Heading, Text, useToast, Spinner, Image } from '@chakra-ui/react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'

const MotionBox = motion(Box)

function App() {
  const [preview, setPreview] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const toast = useToast()

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (file && file.type.startsWith('image/')) {
      setIsLoading(true)
      setPrediction(null)
      
      // Show preview
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(file)

      // Send to backend
      try {
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('http://localhost:8000/predict', {
          method: 'POST',
          body: formData,
        })

        const data = await response.json()
        
        if (data.error) {
          throw new Error(data.error)
        }

        setPrediction({
          class: data.prediction,
          confidence: data.confidence
        })
        toast({
          title: 'Prediction complete!',
          description: `This looks like ${data.prediction} (${data.confidence} confident)!`,
          status: 'success',
          duration: 5000,
          isClosable: true,
        })
      } catch (error) {
        toast({
          title: 'Error',
          description: error.message,
          status: 'error',
          duration: 5000,
          isClosable: true,
        })
      } finally {
        setIsLoading(false)
      }
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': [],
      'image/png': [],
      'image/webp': []
    },
    multiple: false
  })

  return (
    <Box
      minH="100vh"
      bgGradient="linear(to-b, gray.50, white)"
      py={10}
      px={4}
      position="relative"
    >
      <VStack spacing={12} maxW="container.md" mx="auto" pb={16}>
          <VStack spacing={4}>
            <Box
              p={2}
              display="flex"
              alignItems="center"
              justifyContent="center"
              mb={2}
            >
              <Image
                src="/1.png"
                alt="Axomium Logo"
                height="50px"
                objectFit="contain"
                mb={4}
              />
            </Box>
            <Heading
              as="h1"
              size="2xl"
              bgGradient="linear(to-r, purple.500, pink.500)"
              bgClip="text"
              letterSpacing="tight"
              textAlign="center"
            >
              Axo Food Vision
            </Heading>
            <Text
              color="gray.600"
              textAlign="center"
              fontSize="lg"
              maxW="md"
              lineHeight="tall"
            >
              Upload an image of pizza, steak, or sushi and let our advanced AI model identify it with high accuracy!
            </Text>
          </VStack>
          
          <MotionBox
            {...getRootProps()}
            w="full"
            h="400px"
            border="2px dashed"
            borderColor={isDragActive ? "pink.400" : "gray.200"}
            borderRadius="2xl"
            display="flex"
            alignItems="center"
            justifyContent="center"
            bg="white"
            position="relative"
            cursor="pointer"
            transition="all 0.2s"
            boxShadow="lg"
            _hover={{
              borderColor: "pink.400",
              transform: "translateY(-2px)",
              boxShadow: "xl"
            }}
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
          >
            <input {...getInputProps()} />
            {preview ? (
              <Box position="relative" w="100%" h="100%" display="flex" alignItems="center" justifyContent="center">
                <Box
                  as="img"
                  src={preview}
                  alt="Uploaded food"
                  objectFit="cover"
                  w="100%"
                  h="100%"
                  borderRadius="xl"
                />
                {isLoading && (
                  <Box
                    position="absolute"
                    top="0"
                    left="0"
                    right="0"
                    bottom="0"
                    bg="blackAlpha.50"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                  >
                    <Spinner size="xl" color="green.500" thickness="4px" />
                  </Box>
                )}
                {prediction && !isLoading && (
                  <Box
                    position="absolute"
                    bottom="0"
                    left="0"
                    right="0"
                    p={4}
                    bgGradient="linear(to-t, blackAlpha.800, blackAlpha.600)"
                    color="white"
                    textAlign="center"
                    backdropFilter="blur(8px)"
                  >
                    <VStack spacing={1}>
                      <Text
                        fontSize="2xl"
                        fontWeight="bold"
                        textShadow="0 2px 4px rgba(0,0,0,0.2)"
                      >
                        {prediction.class}
                      </Text>
                      <Text
                        fontSize="md"
                        bgGradient="linear(to-r, purple.200, pink.200)"
                        bgClip="text"
                        fontWeight="semibold"
                      >
                        Confidence: {prediction.confidence}
                      </Text>
                    </VStack>
                  </Box>
                )}
              </Box>
            ) : (
              <VStack spacing={4} p={8} textAlign="center">
                <Box
                  p={6}
                  borderRadius="full"
                  bg="gray.50"
                  border="1px"
                  borderColor="gray.200"
                  boxShadow="inner"
                >
                  <Text
                    fontSize="xl"
                    bgGradient="linear(to-r, purple.600, pink.600)"
                    bgClip="text"
                    fontWeight="semibold"
                  >
                    {isDragActive
                      ? "Drop your food image here"
                      : "Drag & drop your food image here"}
                  </Text>
                </Box>
                <VStack spacing={2}>
                  <Text fontSize="md" color="gray.500" fontWeight="medium">
                    or click to select a file
                  </Text>
                  <Text
                    fontSize="sm"
                    color="gray.400"
                    maxW="80%"
                    textAlign="center"
                    fontStyle="italic"
                  >
                    Supports JPEG, PNG, or WebP images of pizza, steak, or sushi
                  </Text>
                </VStack>
              </VStack>
            )}
          </MotionBox>
      </VStack>
      <Box
        position="fixed"
        bottom={0}
        left={0}
        right={0}
        py={4}
        bgGradient="linear(to-r, gray.50, white, gray.50)"
        borderTop="1px"
        borderColor="gray.100"
        textAlign="center"
        backdropFilter="blur(8px)"
        boxShadow="0 -4px 6px -1px rgba(0, 0, 0, 0.05)"
      >
        <VStack spacing={1}>
          <HStack spacing={2} align="center">
            <Box
              w="32px"
              h="32px"
              bgGradient="linear(to-br, purple.500, pink.500)"
              borderRadius="lg"
              display="flex"
              alignItems="center"
              justifyContent="center"
              transform="rotate(45deg)"
              _hover={{ transform: "rotate(225deg)" }}
              transition="transform 0.5s ease"
            >
              <Text
                transform="rotate(-45deg)"
                color="white"
                fontSize="lg"
                fontWeight="bold"
              >
                A
              </Text>
            </Box>
            <Text
              fontSize="xl"
              fontWeight="bold"
              bgGradient="linear(to-r, purple.500, pink.500)"
              bgClip="text"
              _hover={{
                bgGradient: "linear(to-r, pink.500, purple.500)"
              }}
              transition="all 0.3s ease"
              cursor="pointer"
            >
              Axomium Labs
            </Text>
          </HStack>
          <Text color="gray.600" fontSize="sm">
            Developed and managed with ❤️
          </Text>
        </VStack>
      </Box>
    </Box>
  )
}

export default App
