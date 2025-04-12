import { useState, ChangeEvent } from 'react';
import { Box, Button, Container, Flex, Heading, Input, VStack, Text, Divider } from '@chakra-ui/react';
import { createFileRoute } from '@tanstack/react-router';

// Define the type for history entries
type HistoryEntry = {
  input: string;
  response: any;
};

// Create the route for the ChatPage
export const Route = createFileRoute('/_layout/chatpage')({
  component: ChatPage,
});

function ChatPage() {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
  };

  const handleSubmit = async () => {
    const accessToken = localStorage.getItem('access_token');
    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ input }),
    };

    try {
      const response = await fetch('http://localhost/api/v1/c_gnr', requestOptions);
      const data = await response.json();
      setHistory([...history, { input, response: data }]);
      setInput(''); // Clear the input field after submission
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Container maxW="lg" p={4} centerContent>
      <Heading as="h1" mb={4}>Chat Application</Heading>
      <VStack spacing={4} w="100%">
        <Flex as="form" w="100%" onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
          <Input
            value={input}
            onChange={handleInputChange}
            placeholder="Type your message..."
            flex="1"
            mr={2}
            size="lg"
          />
          <Button onClick={handleSubmit} size="lg">Send</Button>
        </Flex>
        <Box w="100%">
          <Heading as="h2" size="lg" mb={2}>Conversation History:</Heading>
          <Box maxH="300px" overflowY="auto" border="1px" borderColor="gray.200" p={4} borderRadius="md">
            {history.map((entry, index) => (
              <Box key={index} mb={4}>
                <Text><strong>You:</strong> {entry.input}</Text>
                <Text><strong>Bot:</strong> {entry.response}</Text>
                {index < history.length - 1 && <Divider my={2} />}
              </Box>
            ))}
          </Box>
        </Box>
      </VStack>
    </Container>
  );
}

export default ChatPage;
