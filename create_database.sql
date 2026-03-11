-- Script para criação do banco de dados MySQL
-- Execute este script no MySQL Workbench

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS sistema_km;
USE sistema_km;

-- Criar tabela de viagens
CREATE TABLE viagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mes_referencia VARCHAR(7) NOT NULL,
    data_hora DATETIME NOT NULL,
    motorista VARCHAR(100) NOT NULL,
    setor VARCHAR(50) NOT NULL,
    destino VARCHAR(200) NOT NULL,
    km_saida DECIMAL(10,2) NOT NULL,
    km_chegada DECIMAL(10,2) NOT NULL,
    km_percorrida DECIMAL(10,2) NOT NULL,
    modelo_carro VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para melhor performance
CREATE INDEX idx_motorista ON viagens(motorista);
CREATE INDEX idx_data_hora ON viagens(data_hora);
CREATE INDEX idx_setor ON viagens(setor);
CREATE INDEX idx_mes_referencia ON viagens(mes_referencia);