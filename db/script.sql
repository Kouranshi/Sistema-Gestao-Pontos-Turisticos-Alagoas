create table usuario (
id_usuario SERIAL primary key,
nome varchar(255) not null,
email varchar(100) not null unique,
senha_hash varchar(60) not null,
data_cadastro timestamp default current_timestamp
);

create table ponto_turistico (
id_ponto_turistico SERIAL primary key,
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

create table categoria (
id_categoria SERIAL primary key,
nome varchar(45) not null,
descricao text
);

create table ponto_turistico_categoria (
id_ponto_turistico INT not null,
id_categoria INT not null,
foreign key (id_ponto_turistico) references ponto_turistico(id_ponto_turistico),
foreign key (id_categoria) references categoria(id_categoria),
primary key (id_ponto_turistico, id_categoria)
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