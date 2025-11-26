/* Depois de criar o banco de dados (através da main.py ou pelo PostgreSQL, mesmo), é necessário copiar esse código e criar as tabelas no PostgreSQL. */

create table usuario (
id_usuario SERIAL primary key,
nome varchar(255) not null,
email varchar(100) not null unique,
senha_hash varchar(60) not null,
data_cadastro timestamp default current_timestamp
);

create table categoria (
id_categoria SERIAL primary key,
nome varchar(45) not null,
nome_exibicao varchar (45) not null
);

create table ponto_turistico (
id_ponto_turistico SERIAL primary key,
id_categoria int not null,
foreign key (id_categoria) references categoria(id_categoria),
nome varchar(45) not null,
nome_exibicao varchar(100),
descricao text,
horario_funcionamento varchar(45),
custo_entrada decimal(10,2),
logradouro varchar(150),
estado varchar(45) not null,
cidade varchar(45) not null,
cep varchar(10) not null,
latitude decimal(9,6),
longitude decimal(9,6)
);

create table avaliacao (
id_avaliacao SERIAL primary key,
nota int check (nota between 0 and 10) not null,
comentario text,
data_avaliacao timestamp default current_timestamp not null,
id_usuario int not null,
id_ponto_turistico int not null,
foreign key (id_usuario) references usuario(id_usuario),
foreign key (id_ponto_turistico) references ponto_turistico(id_ponto_turistico)
);


INSERT INTO categoria (nome, nome_exibicao)
VALUES
('praia', 'Praia'),
('lagoa', 'Lagoa'),
('museu', 'Museu'),
('mirante', 'Mirante'),
('centro_historico', 'Centro Histórico'),
('parque', 'Parque'),
('ilha', 'Ilha');


INSERT INTO ponto_turistico 
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('praia_do_frances', 'Praia do Francês', 'Uma das praias mais famosas do Nordeste, com águas azuis e barreira de corais.', NULL, 0, 'Praia do Francês', 'Marechal Deodoro', 'AL', '57160-000', -9.7482, -35.8349, 1),

('praia_de_pajuçara', 'Praia de Pajuçara', 'Famosa por suas piscinas naturais e jangadas coloridas.', NULL, 0, 'Avenida Dr. Antônio Gouveia', 'Maceió', 'AL', '57030-170', -9.6658, -35.7089, 1),

('praia_de_ponta_verde', 'Praia de Ponta Verde', 'Praia urbana com águas calmas e coqueiros, excelente para banho.', NULL, 0, 'Avenida Álvaro Otacílio', 'Maceió', 'AL', '57035-180', -9.6570, -35.7004, 1),

('praia_de_ipioca', 'Praia de Ipioca', 'Uma das praias mais paradisíacas de Maceió, abriga o Hibiscus Beach Club.', NULL, 0, 'Praia de Ipioca', 'Maceió', 'AL', '57039-000', -9.5352, -35.6487, 1);


INSERT INTO ponto_turistico 
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('lagoa_mundaú', 'Lagoa Mundaú', 'Uma das maiores lagoas do estado, famosa pelo pôr do sol e os nove núcleos lacustres.', NULL, 0, NULL, 'Maceió', 'AL', '57000-000', -9.6667, -35.7333, 2),

('lagoa_do_paixe', 'Lagoa do Paixe', 'Lagoa de águas tranquilas localizada em Piaçabuçu.', NULL, 0, NULL, 'Piaçabuçu', 'AL', '57210-000', -10.4075, -36.4341, 2);


INSERT INTO ponto_turistico
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('museu_théo_brandao', 'Museu Théo Brandão', 'Museu de antropologia e cultura popular alagoana.', '09h às 17h', 0, 'Av. da Paz, 1490', 'Maceió', 'AL', '57020-320', -9.6643, -35.7339, 3),

('museu_palacio_floriano_peixoto', 'Palácio Floriano Peixoto', 'Antigo palácio do governo, hoje museu histórico.', '09h às 16h', 0, 'Praça Floriano Peixoto', 'Maceió', 'AL', '57020-090', -9.6655, -35.7350, 3);


INSERT INTO ponto_turistico
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('mirante_sao_goncalo', 'Mirante São Gonçalo', 'Vista panorâmica da cidade de Maceió e do litoral.', NULL, 0, 'R. São Gonçalo', 'Maceió', 'AL', '57000-000', -9.6653, -35.7272, 4);


INSERT INTO ponto_turistico
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('centro_historico_penedo', 'Centro Histórico de Penedo', 'Construções coloniais e igrejas seculares às margens do Rio São Francisco.', NULL, 0, NULL, 'Penedo', 'AL', '57200-000', -10.2918, -36.5858, 5);


INSERT INTO ponto_turistico
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('parque_municipal_maceio', 'Parque Municipal de Maceió', 'Reserva ambiental com trilhas e rica biodiversidade.', '08h às 16h', 0, 'Av. Fernandes Lima', 'Maceió', 'AL', '57057-000', -9.5575, -35.7433, 6);


INSERT INTO ponto_turistico
(nome, nome_exibicao, descricao, horario_funcionamento, custo_entrada, logradouro, cidade, estado, cep, latitude, longitude, id_categoria)
VALUES
('ilha_da_crôa', 'Ilha da Crôa', 'Ilha paradisíaca com águas cristalinas no litoral norte alagoano.', NULL, 0, NULL, 'Barra de Santo Antônio', 'AL', '57925-000', -9.4093, -35.4902, 7);