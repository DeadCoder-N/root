/*
  # Create Contact Messages Table

  1. New Tables
    - `contact_messages`
      - `id` (uuid, primary key)
      - `name` (text, required) - Name of the person contacting
      - `email` (text, required) - Email address for response
      - `subject` (text, required) - Subject of the message
      - `message` (text, required) - The actual message content
      - `created_at` (timestamptz) - Timestamp when message was sent
      - `is_read` (boolean) - Whether the message has been read
  
  2. Security
    - Enable RLS on `contact_messages` table
    - Add policy for anyone to insert messages (public contact form)
    - Add policy for authenticated admin users to read messages
  
  3. Important Notes
    - Public can only INSERT messages (contact form submission)
    - Only authenticated users can view messages (admin access)
    - Messages are ordered by creation date for easy management
*/

CREATE TABLE IF NOT EXISTS contact_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text NOT NULL,
  subject text NOT NULL,
  message text NOT NULL,
  created_at timestamptz DEFAULT now(),
  is_read boolean DEFAULT false
);

ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can submit contact messages"
  ON contact_messages
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view contact messages"
  ON contact_messages
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Authenticated users can update read status"
  ON contact_messages
  FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_contact_messages_created_at ON contact_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contact_messages_is_read ON contact_messages(is_read);
